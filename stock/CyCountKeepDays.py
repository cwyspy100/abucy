# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


def getFilePath(dir_path):
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    # 输出结果
    # for file in all_files:
    #     print(file)
    return all_files


def count_keep_days(file_path):
    # 假设您的股票数据保存在一个 CSV 文件中
    # 数据格式应包括日期和收盘价，示例 CSV 文件名为 'stock_data.csv'
    # CSV 文件的日期列应命名为 'Date'
    # 收盘价列应命名为 'Close'

    # 使用 split 方法提取
    stock_code = file_path.split('/')[-1].split('_')[0]

    # 读取股票数据

    try:
        df = pd.read_csv(file_path)
    except Exception:
        return

    # 确保日期列是日期时间格式
    df['date'] = pd.to_datetime(df['date'])

    # 按日期排序
    df.sort_values('date', inplace=True)

    # 计算 60 日均线
    df['60_MA'] = df['close'].rolling(window=60).mean()

    # 寻找 60日均线大于股价的时间段
    df['Condition'] = df['60_MA'] <= df['close']

    # 识别条件变化的开始和结束
    df['Group'] = (df['Condition'] != df['Condition'].shift()).cumsum()

    # 找出满足条件的组
    groups = df[df['Condition']].groupby('Group')

    # 统计开始时间、结束时间和持续天数，并计算涨跌幅
    results = []

    for name, group in groups:
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

        results.append((stock_code, start_date.date(), end_date.date(), duration, change_percent))

    # 将结果转换为 DataFrame
    results_df = pd.DataFrame(results, columns=['代码', '开始时间', '结束时间', '持续天数', '涨跌幅'])
    # 将结果写入 CSV 文件
    results_df.to_csv('results.csv', header=False, index=False, encoding='utf-8-sig', mode='a')

    # 初始化计数器
    less_than_5_days = 0
    greater_than_5_days = 0

    # 统计持续天数
    for _, _, _, duration, _ in results:
        if duration < 5:
            less_than_5_days += 1
        else:
            greater_than_5_days += 1

    # 创建一个 DataFrame 存储结果
    # 追加写入 CSV 文件
    summary_df = pd.DataFrame({
        '代码': [stock_code],
        '持续天数小于5': [less_than_5_days],
        '持续天数大于或等于5': [greater_than_5_days]
    })

    summary_df.to_csv('results_count.csv', mode='a', index=False, header=False)


    print("结果已写入 results.csv")

if __name__ == '__main__':
    directory_path = 'D:/abu/cn/stock/'
    file_path = getFilePath(directory_path)
    for file in file_path:
        print(file)
        count_keep_days(file)