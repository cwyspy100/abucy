# 获取市场的实时行情


import pandas as pd
import akshare as ak
from datetime import date
import os
import time
from util import RegUtil, PathUtil


# 1. 获取股票的实时行情
def get_all_latest_convert_bond():
    current_date = date.today()
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"abu/cn/all/bond_{current_date}.csv"
    file_path = PathUtil.get_user_path(file_name)
    bond_data = None
    if os.path.exists(file_path):
        bond_data = pd.read_csv(file_path)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        bond_data = ak.bond_zh_hs_cov_spot()
        bond_data.to_csv(file_path, index=False)
    return bond_data

def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"abu/cn/bond/{symbol}_{start_date}_{end_date}"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}
    file_path = PathUtil.get_user_path(file_name)
    # print("file_name size : {}".format(os.path.getsize(file_name)))
    if os.path.exists(file_path) and os.path.getsize(file_path) > 2:
        try:
            bond_tmp_data = pd.read_csv(file_path)
            return bond_tmp_data
        except Exception as e:
            print(f"读取文件失败，错误信息：{e}")
            return None
    else:
        return None



"""
todo list
1、获取20240416的数据 get_all_latest_stock()
2、更新个单数据update_all_stock_data_simple("20230410", "20240415", "20240416")
3、选股，1，2,3 可以同时，但是 4  需要单独执行
"""
if __name__ == '__main__':
    start = time.time()
    current_date = 20240531
    # 周一减少3天
    check_date = current_date - 1

    # # # 1、获取股票的实时行情
    get_all_latest_convert_bond()

    # 4、回测股票
    print("time cost:", time.time() - start)
