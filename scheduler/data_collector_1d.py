import sys
from datetime import datetime
from agent.Connect import LS
from db_handler.mongodb_handler import MongoDBHandler

ebest = LS("DEMO")
ebest.login()

mongodb = MongoDBHandler()

def collect_code_list():
    result = ebest.get_code_list("ALL")
    mongodb.delete_items({}, "stocklab", "code_info")
    mongodb.insert_items(result, "stocklab", "code_info")

def collect_stock_info():
    code_list = mongodb.find_items({}, "stocklab", "code_info")
    target_code = set([item["단축코드"] for item in code_list])
    today = datetime.today().strftime("%Y%m%d")
    collect_list = mongodb.find_items({"날짜":today}, "stocklab", "prinf_info").distinct("code")
    
    for col in collect_list:
        target_code.remove(col)
    
    for code in target_code:
        result_price = ebest.get_stock_price_by_code(code, "1")
        if len(result_price) > 0:
            mongodb.insert_items(result_price, "stocklab", "price_info")

if __name__ == "__main__":
    collect_code_list()
    collect_stock_info()