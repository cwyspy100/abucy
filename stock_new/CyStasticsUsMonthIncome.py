import pandas as pd
import os
from datetime import datetime, timedelta
import time
import numpy as np

"""
这个程序统计了，上个月收益前10的股票，下个月持有，统计一年发现收益是-99%
这个策略在A股上基本上行不通。上个月涨，下个月基本都大跌了。

"""


# 设置股票数据文件夹路径
# FOLDER_PATH = '/Users/water/abu/cn/stock/'
FOLDER_PATH = '/Users/water/abu/csv_his/'

def is_file(path):
    """判断给定路径是否是文件"""
    return os.path.isfile(path)

def is_file_with_prefix(filename, prefix='us'):
    """判断文件名是否以指定前缀开头"""
    return filename.startswith(prefix) and filename.split("_")[0] == 'usVRTB'

def read_stock_data(folder_path):
    """读取文件夹下所有股票数据并返回一个字典，键为股票名，值为 DataFrame"""
    stock_data = {}
    index = 0
    for filename in os.listdir(folder_path):
        if is_file_with_prefix(filename):
            print("filename {}".format(filename))
            # stock_name = filename[:-4]  # 去掉文件扩展名
            stock_name = filename.split('_')[0]  # 提取股票代码，例如 '001319'
            file_path = os.path.join(folder_path, filename)
            pd_data = pd.read_csv(file_path, parse_dates=['date'])
            if pd_data is None:
                continue
            stock_data[stock_name] = pd_data
            # index = index + 1
            # if index == 100:
            #     break
    return stock_data

def calculate_monthly_returns(stock_data):
    """计算每个月的收益，并返回一个字典，键为月份，值为收益数据"""
    monthly_returns = {}
    for stock_name, data in stock_data.items():
        data.set_index('date', inplace=True)
        data['monthly_return'] = data['close'].pct_change()
        data['month'] = data.index.to_period('M')
        monthly_return = data.groupby('month')['monthly_return'].sum()
        monthly_returns[stock_name] = monthly_return
    return monthly_returns

def get_top_stocks(monthly_returns, month, top_n=10):
    """获取指定月份收益最好的前 N 个股票"""
    month_returns = {stock: returns.get(month, 0) for stock, returns in monthly_returns.items()}
    top_stocks = sorted(month_returns.items(), key=lambda x: x[1], reverse=True)[:top_n]
    return top_stocks

def main():
    stock_data = read_stock_data(FOLDER_PATH)
    monthly_returns = calculate_monthly_returns(stock_data)

    print("month_return {}".format(monthly_returns))

    total_profit = 0.0
    current_date = datetime(2011, 8, 1)  # 开始日期
    end_date = datetime(2017, 8, 1)  # 截止日期

    while current_date < end_date:
        month = current_date.strftime('%Y-%m')
        top_stocks = get_top_stocks(monthly_returns, month)
        print("month {} top_stocks {}", month, top_stocks)

        # 持有前 10 个股票一个月，计算下个月的收益
        for stock, _ in top_stocks:
            # 获取下个月的收益
            next_month = (current_date + pd.DateOffset(months=1)).strftime('%Y-%m')
            next_month_return = monthly_returns[stock].get(next_month, 0)
            if np.isnan(next_month_return) or np.isinf(next_month_return):
                continue
            print("current date {} code {}, return value {}".format(month, stock, next_month_return))
            total_profit += next_month_return  # 收益累加

        current_date += pd.DateOffset(months=1)  # 移动到下一个月份

    print(f"截至 {end_date.date()} 的总收益: {(total_profit/ 10):.2%}")

if __name__ == '__main__':
    start = time.time()
    main()
    # filename = '300210_20230410_20240614'
    # print(filename.find('_'))
    print("cost time {}".format(time.time() - start))