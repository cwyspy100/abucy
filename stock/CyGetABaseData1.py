# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time



# 假设您要读取的文件是一个 CSV 文件
file_path = 'results_monitor_20241028.csv'  # 替换为您的文件路径

# 读取数据
df = pd.read_csv(file_path)

# 确保 '结束时间' 列被解析为日期
df['结束时间'] = pd.to_datetime(df['结束时间'])

# 进行过滤
filtered_df = df[
    (df['结束时间'] == '2024-10-28') &
    (df['持续天数'] > 10) &
    (df['市盈率'] > 5) &
    (df['市盈率'] < 30)
]

# 查看过滤后的结果
print(filtered_df)

# 假设您要读取的文件是一个 CSV 文件
file_path1 = 'Table.xls'
# 读取数据
source_df = pd.read_excel(file_path1)

print(source_df)

