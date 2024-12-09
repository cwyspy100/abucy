# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


def get_stock_data_by_name(symbol, start_date='20100101', end_date='20241113'):
    file_name = f"D:\\abu\\qfq\\cn\\stock\\{symbol}_{start_date}_{end_date}"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}

    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        try:
            stock_data = ak.stock_zh_a_hist(symbol, period='daily', start_date=start_date, end_date=end_date, adjust="qfq")
            stock_data = stock_data.rename(columns=column_names)
            selected_columns = stock_data.filter(items=column_names.values())
            selected_columns.to_csv(file_name, index=False)
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data



if __name__ == '__main__':
    df = get_stock_data_by_name("300033")
    # print(stock_data.head())
    # df = pd.DataFrame(stock_data)
    df['date'] = pd.to_datetime(df['date'])
    # 提取每年的年初和年末价格
    annual_data = df.groupby(df['date'].dt.year).agg({'close': ['first', 'last']})
    # 计算涨幅
    annual_data['涨幅'] = (annual_data['close']['last'] - annual_data['close']['first']) / annual_data['close'][
        'first'] * 100
    print(annual_data['涨幅'])