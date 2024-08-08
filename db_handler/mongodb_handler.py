from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser

class MongoDBHandler:
    def __init__(self):
        """
        config.ini 파일에서 MongoDB 접속 정보를 로딩
        접속 정볼르 이용해 MongoDB 접속에 사용할 client 생성
        """
        config = configparser.ConfigParser()
        config.read('config/config.ini')
        host = config['MONGODB']['host']
        port = config['MONGODB']['port']

        self._client = MongoClient(host, int(port))

    def insert_item(self, data, db_name=None, collection_name=None):
        """
        MongoDB에 document를 입력받기 위한 method
        :param datas: dict: document를 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return inserted_id: str: 입력 완료된 ObjectID를 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if not isinstance(data, dict):
            raise Exception("data type should be dict")
        if db_name is None or collection_name is None:
            raise Exception("Need to be param db_name, collection_name")
        return self._client[db_name][collection_name].insert_one(data).inserted_id
    
    def insert_items(self, datas, db_name=None, collection_name=None):
        """
        MongoDB에 여러 개의 document를 입력받기 위한 method
        :param datas: dict: document의 list를 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return inserted_id: str: 입력 완료된 ObjectID를 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if not isinstance(datas, list):
            raise Exception("datas type should be list")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].insert_many(datas).inserted_ids
    
    def find_item(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에 document를 검색
        :param condition: dict: 검색 조건을 dict 형태로 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return document: dict: 검색된 문서가 있으면 문서의 내용을 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if condition is None or not isinstance(condition, dict):
            condition = {}
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].find_one(condition)
    
    def find_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에 여러 개의 document를 검색
        :param condition: dict: 검색 조건을 dict 형태로 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return Cursor: cursor를 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if condition is None or not isinstance(condition, dict):
            condition = {}
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)
    
    def delete_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에 여러 개의 document를 삭제하기 위한 method
        :param condition: dict: 삭제 조건을 dict 형태로 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return DeleteResult: obj: PyMongo의 문서 삭제 결과 객체인 DeleteResult가 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if condition is None or not isinstance(condition, dict):
            raise Exception("Need to condition")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].delete_many(condition)
    
    def update_item(self, condition=None, update_value=None, db_name=None, collection_name=None, upsert=True):
        """
        MongoDB에 하나의 document를 갱신하기 위한 method
        :param condition: dict: 갱신 조건을 dict 형태로 받음
        :param update_value: dict: 갱신하고자 하는 값을 dict 형태로 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return UpdateResult: obj: PyMongo의 문서 갱신 결과 객체인 UpdateResult가 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if condition is None or not isinstance(collection, dict):
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].update_one(filter=condition, update=update_value, upsert=True)
    
    def update_items(self, condition=None, update_value=None, db_name=None, collection_name=None, upsert=True):
        """
        MongoDB에 여러 개의 document를 갱신하기 위한 method
        :param condition: dict: 갱신 조건을 dict 형태로 받음
        :param update_value: dict: 갱신하고자 하는 값을 dict 형태로 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음
        :return UpdateResult: obj: PyMongo의 문서 갱신 결과 객체인 UpdateResult가 반환
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if condition is None or not isinstance(collection, dict):
            raise Exception("Need to condition")
        if update_value is None:
            raise Exception("Need to update value")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].update_many(filter=condition, update=update_value)
    
    def aggregate(self, pipeline=None, db_name=None, collection_name=None):
        """
        MongoDB의 aggregate작업을 위한 method
        :param pipeline: list: 갱신 조건을 dict의 list형태로 받음
        :param db_name: str: MongoDB에서 db에 해당하는 이름을 받음
        :param collection_name: str: db에 속하는 collection 이름을 받음        
        :return CommandCursor: obj: PyMongo이 CommandCursor가 반환됨
        :raises Exception: 매개변수 db_name과 collection_name이 없으면 Exception발생
        """
        if pipeline is None or not isinstance(pipeline, list):
            raise Exception("Need to pipeline")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].aggregate(pipeline)
    
    def text_search(self, text=None, db_name=None, collection_name=None):
        if text is None or not isinstance(text, str):
            raise Exception("Need to text")
        if db_name is None or collection_name is None:
            raise Exception("Need to param db_name, collection_name")
        return self._client[db_name][collection_name].find({"$text": {"$search":text}})