import configparser
import win32com.client
import pythoncom
from datetime import datetime
import time 

class XASession:
    login_state = 0

    def OnLogin(self, code, msg):
        """
        Login 시도 후 호출
        code == 0000이면 Login Success
        """
        if code == "0000":
            print(code, msg)
            XASession.login_state = 1
        else:
            print(code, msg)
    
    def OnDisconnect(self):
        """
        서버와 연결이 끊어지면 호출
        """
        print("Session disconnected")
        XASession.login_state = 0

class LS:
    QUERY_LIMIT_10MIN = 200
    LIMIT_SECONDS = 600

    def __init__(self, mode=None):
        if mode not in ["PROD", "DEMO", "ACE"]:
            raise Exception("Need to run_mode(PROD or DEMO or ACE)")
        
        run_mode = "EBST_" + mode
        config = configparser.ConfigParser()
        config.read('conf/config.ini', encoding='utf8')

        self.user = config[run_mode]['user']
        self.passwd = config[run_mode]['password']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)
        self.query_cnt = []

    def login(self):
        self.xa_session_client.ConnectServer(self.host, self.port)
        self.xa_session_client.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()
        
    def logout(self):
        XASession.login_state = 0
        self.xa_session_client.DisconnectServer()

    def execute_query(self, res, in_block_name, out_block_name, *out_fields, **set_fields):
        """
        TR code 실행 method
        :param res:            str 리소스 이름(TR)
        :param in_block_name:  str 인블록 이름
        :param out_block_name: str 아웃블록 이름
        :param out_params:     list 출력 필드 리스트
        :param in_params:      dict 인 블록에 설정할 필드 딕셔너리
        :param result:         list 결과를 list에 담아 반환
        """
        time.sleep(1)
        print("current query cnt: ", len(self.query_cnt))
        print(res, in_block_name, out_block_name)
        while len(self.query_cnt) >= LS.QUERY_LIMIT_10MIN:
            time.sleep(1)
            print("waiting for execute query... current query cnt: ", len(self.query_cnt))
            self.query_cnt = list(filter(lambda x: (datetime.today() - x).total_seconds() < LS.LIMIT_SECONDS, self.query_cnt))

        xa_query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        xa_query.LoadFromResFile(XAQuery.RES_PATH + res + ".res")

        # in_block setting
        for key, value in set_fields.items():
            xa_query.SetFieldData(in_block_name, key, 0, value)
        errorCode = xa_query.Request(0)

        # 요청 후 대기
        waiting_cnt = 0
        while xa_query.tr_run_state == 0:
            waiting_cnt += 1
            if waiting_cnt % 100000 == 0:
                #print("Waiting...", self.xa_session_client.GetLastError())
                pass
            pythoncom.PumpWaitingMessages()
        
        # 결과 블록
        result = []
        count = xa_query.GetBlockCount(out_block_name)

        for i in range(count):
            item = {}
            for field in out_fields:
                value = xa_query.GetFieldData(out_block_name, field, i)
                item[field] = value
            result.append(item)
        
        # 제약시간 체크
        XAQuery.tr_run_state = 0
        self.query_cnt.append(datetime.today())

        # 영문 필드명을 한글명으로 전환
        for item in result:
            for field in list(item.keys()):
                if getattr(field, res, None):
                    res_field = getattr(field, res, None)
                    if out_block_name in res_field:
                        field_hname = res_field[out_block_name]
                        if field in field_hname:
                            item[field_hname[field]] = item[field]
                            item.pop(field)
        return result

    def get_code_list(self, market=None):
        """
        TR: 8436
        :param market: str 전체(0), KOSPI(1), KOSDAQ(2)
        :return result: list 시장별 종목 리스트
        """
        if market not in ["ALL", "KOSPI", "KOSDAQ"]:
            raise Exception("Need to market param(ALL, KOSPI, KOSDAQ)")

        market_code = {"ALL":"0", "KOSPI":"1", "KOSDAQ":"2"}
        in_params = {"gubun":market_code[market]}
        out_params = ['hname', 'shcode', 'expcode', 'etfgubun', 'memedan', 'gubun', 'spac_gubun']

        return self.execute_query("t8436", 
                                  "t8436InBlock", 
                                  "t8436OutBlock", 
                                  *out_params, 
                                  **in_params)

    def get_stock_price_by_code(self, code=None, cnt="1"):
        """
        TR: t1305 현재 날짜를 기준으로 cnt만큼 전일의 데이터를 가져온다.
        :param code: str 종목코드
        :param cnt: str 이전 데이터 조회 범위(일단위)
        :param result: list 종목의 최근 가격 정보
        """
        tr_code = "t1305"
        in_params = {"shcode":code, "dwmcode":"1", "date":"", "idx":"", "cnt":cnt}
        out_params = ['date', 'open', 'high', 'low', 'close', 'sign', 'change', 'diff',
                      'volume', 'diff_vol', 'chdegree', 'sojinrate', 'changerate', 'fpvolume',
                      'covolume', 'value', 'ppvolume', 'o_sign', 'o_change', 'o_diff',
                      'h_sign', 'h_change', 'h_diff', 'l_sign', 'l_change', 'l_diff', 'marketcap']
        result = self.execute_query("t1305",
                                    "t1305InBlock",
                                    "t1305OutBlock1",
                                    *out_params,
                                    **in_params)

        for item in result:
            item["code"] = code
        return result
    
    def get_credit_trend_by_code(self, code=None, date=None):
            """
            TR: t1921 신용거래 동향
            :param code: str 종목코드
            :param date: str 날짜
            """
            in_params = {"gubun":"0", "shcode":code, "date":date, "idx":0}
            out_params = ["mmdate", "close", "sign", "jchange", "diff", "nvolume",
                          "svolume", "jvolume", "price", "change", "gyrate", "jkrate", "shcode"]
            result = self.execute_query("t1921",
                                        "t1921InBlock",
                                        "t1921OutBlock1",
                                        *out_params,
                                        **in_params)
            for item in result:
                item["code"] = code
            return result

    def get_agent_trend_by_code(self, code=None, fromdt=None, todt=None):
        """
        TR: t1717 외인 기관별 종목별 동향
        :param code: str 종목코드
        :param fromdt: str 조회 시작 날짜
        :param todt: str 조회 종료 날짜
        :return result: list 시장별 종목 리스트
        """
        in_params = {"gubun":"0", "fromdt":fromdt, "todt":todt, "shcode":code}
        out_params = ["date", "close", "sign", "change", "diff", "volume",
                      "tjj0000_vol", "tjj0001_vol", "tjj0002_vol", "tjj0003_vol",
                      "tjj0004_vol", "tjj0005_vol", "tjj0006_vol", "tjj0007_vol",
                      "tjj0008_vol", "tjj0009_vol", "tjj0010_vol", "tjj0011_vol",
                      "tjj0018_vol", "tjj0016_vol", "tjj0017_vol", "tjj0001_dan",
                      "tjj0002_dan", "tjj0003_dan", "tjj0004_dan", "tjj0005_dan",
                      "tjj0006_dan", "tjj0007_dan", "tjj0008_dan", "tjj0009_dan",
                      "tjj0010_dan", "tjj0011_dan", "tjj0018_dan", "tjj0016_dan",
                      "tjj0017_dan"]

        for item in result:
            item["code"] = code
        return result

    def get_short_trend_by_code(self, code=None, sdate=None, edate=None):
        """
        TR: 1927 공매도 일별 추이
        :param code: str 종목 코드
        :param sdate: str 시작 일자
        :param edate: str 종료 일자
        :return result: list 시장 별 종목 리스트
        """
        in_params = {"date":sdate, "sdate":sdate, "edate":edate, "shcode":code}
        out_params = ["date", "price", "sign", "change", "diff", "volume", "value",
                      "gm_vo", "gm_va", "gm_per", "gm_avg", "gm_vo_sum"]
        
        result = self.execute_query("t1927",
                                    "t1927InBlock",
                                    "t1927OutBlock1",
                                    *out_params,
                                    **in_params)
        for item in result:
            item["code"] = code
        return result

class XAQuery:
    RES_PATH =  "C:\\LS_SEC\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData", code)
        XAQuery.tr_run_state = 1
    
    def OnReceiveMessage(self, error, code, message):
        print("OnreceiveMessage", error, code, message, XAQuery.tr_run_state)