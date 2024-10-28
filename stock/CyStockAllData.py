# -*- encoding: utf-8 -*-

import akshare as ak
import time
# from util import PathUtil
from datetime import date


def get_all_A_latest_stock():
    """
    只用于获取当天实时的行情
    :return:
    """
    current_date = date.today()
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"/Users/water/abu/cn/all/{current_date}.csv"
    # file_path = PathUtil.get_user_path(file_name)
    stock_data = ak.stock_zh_a_spot_em()
    stock_data.to_csv(file_name, index=False)
    return stock_data


def get_all_HK_latest_stock():
    """
    只用于获取当天实时的行情
    :return:
    """
    current_date = date.today()
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"/Users/water/abu/hk/all/{current_date}.csv"
    stock_data = ak.stock_hk_spot()
    stock_data.to_csv(file_name, index=False)
    return stock_data


# def get_all_US_latest_stock():
#     """
#     只用于获取当天实时的行情
#     :return:
#     """
#     current_date = date.today()
#     current_date = current_date.strftime('%Y%m%d')
#     file_name = f"/Users/water/abu/hk/all/{current_date}.csv"
#     stock_data = ak.stock_hk_spot()
#     stock_data.to_csv(file_name, index=False)
#     return stock_data



# /Users/water/PycharmProjects/abucy/stock/CyStockAllData.py


if __name__ == '__main__':
    """
    进行选股,主要测试通过价格和成交量选股
    """
    start_time = time.time()
    get_all_A_latest_stock()
    get_all_HK_latest_stock()
    end_time = time.time()
    print(f"耗时：{end_time - start_time}")
