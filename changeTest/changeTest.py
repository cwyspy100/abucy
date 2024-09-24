

import pandas as pd
import os

# 文件夹路径
folder_path = '/Users/water/abu/data/csv'

# 存储所有股票数据
all_data = []

# 遍历文件夹，读取所有以 'sz' 开头的文件
index = 0
for filename in os.listdir(folder_path):
    if filename.startswith('sh'):
        file_path = os.path.join(folder_path, filename)
        # 读取文件，假设文件中有 '日期' 和 '收盘价' 列
        df = pd.read_csv(file_path)
        df['股票代码'] = filename.split('_')[0]  # 使用文件名作为股票代码
        df['日期'] = df.iloc[0:, 0]
        all_data.append(df)
        # index = index+1
        # if index > 10:
        #     break

# 合并所有数据
combined_data = pd.concat(all_data, ignore_index=True)

# 确保日期列为日期格式
combined_data['日期'] = pd.to_datetime(combined_data['日期'])

# 提取年份
combined_data['年份'] = combined_data['日期'].dt.year

# 计算每年的收盘价波动
annual_data = combined_data.groupby(['股票代码', '年份'])['close'].agg(['first', 'last']).reset_index()
annual_data['涨幅'] = (annual_data['last'] - annual_data['first']) / annual_data['first'] * 100

# 找出每年涨幅最大的 30 个股票
top_stocks_per_year = annual_data.groupby('年份').apply(lambda x: x.nlargest(10, '涨幅')).reset_index(drop=True)

# 获取下一年的涨幅
next_year_performance = []

for year in top_stocks_per_year['年份'].unique():
    current_year_stocks = top_stocks_per_year[top_stocks_per_year['年份'] == year]['股票代码']
    next_year = year + 1

    for stock in current_year_stocks:
        next_year_data = annual_data[(annual_data['股票代码'] == stock) & (annual_data['年份'] == next_year)]
        if not next_year_data.empty:
            next_year_change = next_year_data['涨幅'].values[0]
            next_year_performance_record = {
                '股票代码': stock,
                '当前年份': year,
                '涨幅': top_stocks_per_year[top_stocks_per_year['年份'] == year][top_stocks_per_year['股票代码'] == stock]['涨幅'].values[0],
                '下一年涨幅': next_year_change
            }
            next_year_performance.append(next_year_performance_record)

# 转换为 DataFrame
result_df = pd.DataFrame(next_year_performance)
result_df.to_csv('result_df_sh.csv', index=False, encoding='utf-8')
# 输出结果
print("result_df save finish")