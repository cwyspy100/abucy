# -*- encoding: utf-8 -*-

import pandas as pd
import akshare as ak
from sqlalchemy import create_engine

# 数据库配置
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'wealth_data'

# 创建数据库连接
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


# 获取股票数据的函数
def fetch_stock_data(stock_code):
    # 获取历史数据
    stock_data = ak.stock_zh_a_daily(symbol=stock_code, adjust="")  # 前复权数据
    stock_data.reset_index(inplace=True)  # 重置索引以便后续使用
    return stock_data


# 插入数据的函数
def insert_stock_data(stock_name, data):
    # 选择需要插入的列
    data_to_insert = data[['date', 'open', 'close', 'high', 'low', 'volume']]
    data_to_insert['stock_name'] = stock_name  # 添加股票名称列
    data_to_insert['date'] = pd.to_datetime(data_to_insert['date'])  # 确保日期格式正确

    # 添加创建时间和更新时间
    data_to_insert['created_at'] = pd.Timestamp.now()  # 当前时间
    data_to_insert['updated_at'] = pd.Timestamp.now()  # 当前时间
    data_to_insert['deleted'] = 0  # 未删除标记

    # 将数据插入到 MySQL
    data_to_insert.to_sql(';', con=engine, if_exists='append', index=False)


# 主程序
if __name__ == '__main__':
    stock_code = '000001.SZ'  # 更改为您想要获取的股票代码
    stock_name = '平安银行'  # 股票名称，可以通过股票代码查找

    # 获取股票数据
    stock_data = fetch_stock_data(stock_code)

    # 插入数据到数据库
    insert_stock_data(stock_name, stock_data)

    print("数据插入成功！")