# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


stock_data = pd.read_csv("20241108.csv")
# print(stock_data.info)
# print(stock_data.columns)

# 转换 '结束时间' 列为日期格式
stock_data['结束时间'] = pd.to_datetime(stock_data['结束时间'])

# 筛选出结束时间为 2024-11-08 的数据
filtered_data = stock_data[stock_data['结束时间'] == '2024-11-08']

# # 按总市值排序并取前 100 条记录
top_100 = filtered_data.nlargest(400, '年初至今涨跌幅')

# 初始化列表以存储每组的平均结果
averages = []

# 使用 for 循环每 10 个计算一次
for i in range(0, len(top_100), 10):
    group = top_100.iloc[i:i + 10]  # 获取当前组
    avg_results = {
        '年初至今涨跌幅': group['年初至今涨跌幅'].mean(),
        '总市值': group['总市值'].mean(),
        '市盈率': group['市盈率'].mean(),
        '市净率': group['市净率'].mean(),
        '持续天数': group['持续天数'].mean()
    }
    averages.append(avg_results)  # 将结果添加到列表中

# 输出每组的平均结果
for index, avg in enumerate(averages):
    print(f"Group {index + 1}: {avg}")