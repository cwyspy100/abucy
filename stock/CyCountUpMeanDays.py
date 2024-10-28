import akshare as ak
import time
import pandas as pd

import datetime
from util import PathUtil
import os







def get_file_path(dir_path):
    # 查询所有文件
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            all_files.append(os.path.join(root, file))
            # 输出结果
    for file in all_files:
        print(file)

# stock_data = ak.stock_zh_a_hist('300059', period='daily', start_date='20220101', end_date='20241023', adjust="")
# stock_data.to_csv('300059.csv')
#
# stock_data = ak.stock_us_hist('106.BRK_B', period='daily', start_date='20220101', end_date='20241022', adjust="")
# stock_data.to_csv('106.BRK_B.csv')
#
# stock_data = ak.stock_hk_hist(symbol="03690", period="daily", start_date="20220101", end_date="20241022", adjust="")
# stock_data.to_csv('03690.csv')

def pick_stock_current_mean(stock_path):
    # 读取股票数据
    try:
        df = pd.read_csv(stock_path)
    except Exception:
        return

    # 确保日期列是日期时间格式
    df['日期'] = pd.to_datetime(df['日期'])

    # 按日期排序
    df.sort_values('日期', inplace=True)

    # 计算 60 日均线
    df['60_MA'] = df['收盘'].rolling(window=60).mean()

    # 寻找 60日均线小于股价的时间段
    df['Condition'] = df['60_MA'] < df['收盘']

    # 识别条件变化的开始和结束
    df['Group'] = (df['Condition'] != df['Condition'].shift()).cumsum()

    # 找出满足条件的组
    groups = df[df['Condition']].groupby('Group')

    # 统计开始时间、结束时间和持续天数
    results = []

    # 获取最后一组的数据
    last_group_key = groups.groups.keys() # 使用 get_group 获取最后一组
    print(list(last_group_key)[-1])
    last_group = groups.get_group(list(last_group_key)[-1])

    start_date = last_group['日期'].iloc[0]
    end_date = last_group['日期'].iloc[-1]
    duration = (end_date - start_date).days + 1  # 包括结束当天

    # 计算涨跌幅
    start_price = last_group['收盘'].iloc[0]
    end_price = last_group['收盘'].iloc[-1]
    if start_price != 0:  # 防止除以零
        change_percent = ((end_price - start_price) / start_price) * 100
        change_percent = f"{change_percent:.2f}%"  # 保留两位小数并加上 %
    else:
        change_percent = None

    results.append((start_date.date(), end_date.date(), duration, change_percent))

    # 输出结果
    for start, end, duration, change_percent in results:
        print(f"开始时间: {start}, 结束时间: {end}, 持续天数: {duration}天, 涨跌幅: {change_percent}")




# if __name__ == '__main__':
#     # 设置要查询的目录路径
#     directory_path = '/Users/water/abu/cn/stock'
#     get_file_path(directory_path)