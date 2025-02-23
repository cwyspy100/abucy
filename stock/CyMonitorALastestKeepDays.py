# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time
from datetime import datetime


def getFilePath(dir_path):
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            all_files.append(os.path.join(root, file))

    # 输出结果
    # for file in all_files:
    #     print(file)
    return all_files



def count_keep_days(file_path, current_data_path, results = []):
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
    stock_name = current_stock_data['名称'].values[0]
    change_60 = current_stock_data['60日涨跌幅'].values[0]
    change_total = current_stock_data['年初至今涨跌幅'].values[0]
    pe = current_stock_data['市盈率-动态'].values[0]
    pb = current_stock_data['市净率'].values[0]
    total_money = current_stock_data['总市值'].values[0] / 100000000
    change_5 = calculate_percentage_change(df['close'].values[-5:])
    change_10 = calculate_percentage_change(df['close'].values[-10:])
    change_20 = calculate_percentage_change(df['close'].values[-20:])
    change_30 = calculate_percentage_change(df['close'].values[-30:])

    # if pe < 0:
    #     return
    # if pb < 0:
    #     return
    # if total_money <= 0:
    #     return

    # 确保日期列是日期时间格式
    df['date'] = pd.to_datetime(df['date'])

    # 按日期排序
    df.sort_values('date', inplace=True)

    # 计算 60 日均线
    df['60_MA'] = df['close'].rolling(window=120).mean()

    df['daily_change'] = df['close'].pct_change() * 100  # 计算百分比变化
    df['daily_change'] = df['daily_change'].round(2)  # 四舍五入到小数点后两位
    df['adjusted_change'] = df['daily_change'].apply(lambda x : 1 if x > 0 else -1 )

    # 寻找 60日均线大于股价的时间段
    df['Condition'] = df['60_MA'] <= df['close']

    # 识别条件变化的开始和结束
    df['Group'] = (df['Condition'] != df['Condition'].shift()).cumsum()

    # 找出满足条件的组
    groups = df[df['Condition']].groupby('Group')

    # 统计开始时间、结束时间和持续天数，并计算涨跌幅
    up_days = 0
    down_days = 0
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

        positive_change_count = (group['adjusted_change'] >= 0).sum()
        negative_change_count = (group['adjusted_change'] < 0).sum()

        change_radio = 1
        if negative_change_count > 0:
            change_radio = round(positive_change_count / negative_change_count, 2)

        results.append((stock_code, stock_name, end_price, start_date.date(), end_date.date(), duration, pe, pb, total_money
                        , change_percent, change_5, change_10, change_20, change_30, change_60, change_total,positive_change_count, negative_change_count, change_radio))

    # # 将结果转换为 DataFrame
    # results_df = pd.DataFrame(results, columns=['代码', '开始时间', '结束时间', '持续天数', '涨跌幅'])
    # # 将结果写入 CSV 文件
    # results_df.to_csv('D:/abu/cn/all/results.csv', header=False, index=False, encoding='utf-8-sig', mode='a')

    # # 初始化计数器
    # less_than_5_days = 0
    # greater_than_5_days = 0
    #
    # # 统计持续天数
    # for _, _, _, duration, _ in results:
    #     if duration < 5:
    #         less_than_5_days += 1
    #     else:
    #         greater_than_5_days += 1
    #
    # # 创建一个 DataFrame 存储结果
    # # 追加写入 CSV 文件
    # summary_df = pd.DataFrame({
    #     '代码': [stock_code],
    #     '持续天数小于5': [less_than_5_days],
    #     '持续天数大于或等于5': [greater_than_5_days]
    # })
    #
    # summary_df.to_csv('D:/abu/cn/all/results_count.csv', mode='a', index=False, header=False)
    # print("结果已写入 results.csv")

# 计算涨幅的函数
def calculate_percentage_change(prices):
    return round(((prices[-1] - prices[0]) / prices[0]) * 100, 2)




if __name__ == '__main__':
    start = time.time()
    directory_path = 'D:/abu/cn/stock/'
    current_data_path = 'D:/abu/cn/all/20250103.csv'
    file_path = getFilePath(directory_path)
    results = []
    for file in file_path:
        print(file)
        count_keep_days(file, current_data_path, results)

    # 将结果转换为 DataFrame
    results_df = pd.DataFrame(results,
                              columns=['代码', '名称', '收盘价', '开始时间', '结束时间', '持续天数', '市盈率', '市净率',
                                       '总市值', '涨跌幅', '5日涨跌幅','10日涨跌幅','20日涨跌幅','30日涨跌幅', '60日涨跌幅', '年初至今涨跌幅', '上涨天数', '下跌天数', '涨幅天数比率'])
    # 将结果写入 CSV 文件
    results_df.to_csv('D:/abu/cn/all/results_monitor_20250103.csv', index=False, encoding='utf-8-sig')

    # count_keep_days('D:/abu/cn/stock/300046_20230101_20241025', current_data_path)

    print("execute cost time {}".format(time.time() - start))



