# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time
from datetime import datetime


def getFilePath(directory_path):
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    # 输出结果
    # for file in all_files:
    #     print(file)
    return all_files


def monitor_keep_days(file_path, current_data_path, results=[]):
    # 假设您的股票数据保存在一个 CSV 文件中
    # 数据格式应包括日期和收盘价，示例 CSV 文件名为 'stock_data.csv'
    # CSV 文件的日期列应命名为 'Date'
    # 收盘价列应命名为 'Close'

    # 使用 split 方法提取
    stock_code = file_path.split('/')[-1].split('_')[0]

    # 读取股票数据
    try:
        df = pd.read_csv(file_path)
        current_df = pd.read_csv(current_data_path, dtype={'代码': str})
    except Exception:
        return

    current_stock_data = current_df[(current_df['代码'] == stock_code)]
    name = current_stock_data['名称'].values[0]
    change_60 = current_stock_data['60日涨跌幅'].values[0]
    change_total = current_stock_data['年初至今涨跌幅'].values[0]
    pe = current_stock_data['市盈率-动态'].values[0]
    pb = current_stock_data['市净率'].values[0]
    total_money = current_stock_data['总市值'].values[0] / 100000000

    if pe < 0:
        return
    if pb < 0:
        return
    if total_money <= 0:
        return

    # 确保日期列是日期时间格式
    df['date'] = pd.to_datetime(df['date'])

    # 按日期排序
    df.sort_values('date', inplace=True)

    # 计算 60 日均线
    df['60_MA'] = df['close'].rolling(window=120).mean()

    # 寻找 60日均线大于股价的时间段
    df['Condition'] = df['60_MA'] <= df['close']

    # 识别条件变化的开始和结束
    df['Group'] = (df['Condition'] != df['Condition'].shift()).cumsum()

    # 找出满足条件的组
    groups = df[df['Condition']].groupby('Group')

    # 统计开始时间、结束时间和持续天数，并计算涨跌幅
    # results = []
    if len(groups.groups.keys()) == 0:
        return

    group = groups.get_group(list(groups.groups.keys())[-1])
    start_date = group['date'].iloc[0]
    end_date = group['date'].iloc[-1]
    duration = (end_date - start_date).days + 1  # 包括结束当天

    # 计算涨跌幅
    start_price = group['close'].iloc[0]
    end_price = group['close'].iloc[-1]
    if start_price != 0:  # 防止除以零
        change_percent = ((end_price - start_price) / start_price) * 100
        change_percent = f"{change_percent:.2f}%"  # 保留两位小数并加上 %
    else:
        change_percent = None

    # target_date = datetime.strptime('2024-06-14', '%Y-%m-%d').date()
    # if end_date.date() == target_date:
    results.append((stock_code, name, start_date.date(), end_date.date(), duration, pe, pb, total_money,
                        change_percent, change_60, change_total))


if __name__ == '__main__':
    start = time.time()
    directory_path = '/Users/water/abu/cn/stock'
    current_data_path = '/Users/water/abu/cn/all/20241024.csv'
    file_path = getFilePath(directory_path)
    results = []
    for file in file_path:
        print(file)
        # count_keep_days(file)
        monitor_keep_days(file, current_data_path, results)

    # 将结果转换为 DataFrame
    results_df = pd.DataFrame(results,
                              columns=['代码', '名称', '开始时间', '结束时间', '持续天数', '市盈率', '市净率',
                                       '总市值', '涨跌幅', '60日涨跌幅', '年初至今涨跌幅'])
    # 将结果写入 CSV 文件
    results_df.to_csv('results_monitor20241122.csv', index=False, encoding='utf-8-sig')

    print("execute cost time {}".format(time.time() - start))
