# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


def get_all_us_stock_data():
    """
        获取所有股票的数据
    """
    stock_data = pd.read_csv('20240424.csv')
    # 循环获取
    for i in stock_data['代码']:
        # 开头是8的股票代码，不处理
        # code = f"{i:06}"
        # if code[0] == '8':
        #     continue
        get_us_stock_data_by_name(i)
        # print()
        # 休息10ms
        time.sleep(0.002)

def get_us_stock_data_by_name(symbol, start_date='20230101', end_date='20250103'):
    file_name = f"D:\\abu\\us\\stock\\{symbol}_{start_date}_{end_date}"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}

    if os.path.exists(file_name):
        try:
            stock_data = pd.read_csv(file_name)
            # stock_data.rename(columns=column_names, inplace=True)
            print('get data from file {}'.format(symbol))
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()
    else:
        try:
            stock_data = ak.stock_us_hist(symbol, period='daily', start_date=start_date, end_date=end_date, adjust="")
            stock_data = stock_data.rename(columns=column_names)
            selected_columns = stock_data.filter(items=column_names.values())
            selected_columns.to_csv(file_name, index=False)
            print('save data to file {}'.format(symbol))
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data




if __name__ == '__main__':
    """
    进行选股,主要测试通过价格和成交量选股
    """
    start_time = time.time()
    # pick_stock(end_date='20240417')
    get_all_us_stock_data()
    end_time = time.time()
    print(f"耗时：{end_time - start_time}")



