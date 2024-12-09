# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


def get_stock_data_by_name(symbol, end_date='20241204'):
    file_name = f"D:\\abu\\hk\\stock\\{symbol}_{end_date}"

    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        try:
            stock_data = ak.stock_hk_daily(symbol=symbol, adjust="")
            stock_data.to_csv(file_name, index=False)
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data


def get_stock_data():
    stock_hk_spot_df = ak.stock_hk_spot()
    stock_hk_spot_df.to_csv("20240613.csv")
    return stock_hk_spot_df


def get_all_stock_data():
    """
        获取所有股票的数据
    """
    stock_data = pd.read_csv('20240613.csv')
    # 循环获取
    for index, row in stock_data.iterrows():
        # 开头是8的股票代码，不处理
        code = f"{row["symbol"]:05}"
        get_stock_data_by_name(code)
        # 休息10ms
        time.sleep(0.01)




if __name__ == '__main__':
    """
    进行选股,主要测试通过价格和成交量选股
    """
    start_time = time.time()
    get_all_stock_data()
    end_time = time.time()
    print(f"耗时：{end_time - start_time}")


