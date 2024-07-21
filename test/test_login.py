import sys
# module의 abs path 지정
sys.path.append("C:\\Users\\SAMSUNG\\Desktop\\toy_project\\stock_lab")

import unittest
from agent.Connect import LS
import inspect, time

class TestAgent(unittest.TestCase):
    def setUp(self):
        self.LS = LS("DEMO")
        self.LS.login()

    def tearDown(self):
        self.LS.logout()

    def test_get_code_list(self):
        print(inspect.stack()[0][3])
        all_result = self.LS.get_code_list("ALL")
        assert all_result is not None
        
        kosdaq_result = self.LS.get_code_list("KOSDAQ")
        assert kosdaq_result is not None
        
        kospi_result = self.LS.get_code_list("KOSPI")
        assert kospi_result is not None
        
        try:
            error_result = self.LS.get_code_list("KOS")
        except:
            error_result = None
        assert error_result is None
        print("result:", len(all_result), len(kosdaq_result), len(kospi_result))
    
    def test_get_stock_price_list_by_code(self):
        print(inspect.stack()[0][3])
        result = self.LS.get_stock_price_by_code("005930", "2")
        assert result is not None
        print(result)

    def test_get_credit_trend_by_code(self):
        print(inspect.stack()[0][3])
        result = self.LS.get_credit_trend_by_code("005930", "20240719")
        assert result is not None
        print(result)

    def test_get_short_trend_by_code(self):
        print(inspect.stack()[0][3])
        result = self.LS.get_short_trend_by_code("005930", sdate="20240701", edate="20240719")
        assert result is not None
        print(result)

    def test_get_agent_trend_by_code(self):
        print(inspect.stack()[0][3])
        result = self.LS.get_agent_trend_by_code("005930", fromdt="20240701", todt="20240719")
        assert result is not None
        print(result)