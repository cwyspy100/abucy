# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


# stock_financial_report_sina_df = ak.stock_financial_report_sina(stock="sh600600", symbol="资产负债表")
# print(stock_financial_report_sina_df.columns)

# stock_financial_report_sina_df.to_csv("sh600600.csv")

# stock_balance_sheet_by_yearly_em_df = ak.stock_balance_sheet_by_yearly_em(symbol="SH600519")
# print(stock_balance_sheet_by_yearly_em_df.columns)


# stock_info_sz_name_code_df = ak.stock_info_sz_name_code(symbol="A股列表")
# print(stock_info_sz_name_code_df)



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
# print(filtered_df)

# # 假设您要读取的文件是一个 CSV 文件
# file_path = 'test.csv'  # 替换为您的文件路径
#
# # 读取数据
# filtered_df = pd.read_csv(file_path)

for code in filtered_df['代码']:
    print(code)
    # print(filtered_df[filtered_df['代码'] == code]['每股净资产'].values[0])
    # if filtered_df[filtered_df['代码'] == code]['每股净资产'].values[0] > 0:
    #     continue
    symbol = f"{code:06}"
    df_other = ak.stock_financial_abstract_ths(symbol=symbol, indicator="按年度")
    if df_other is None:
        continue
    # 获取销售净利率
    # print(stock_financial_abstract_ths_df[['报告期','每股净资产', '销售净利率', '销售毛利率', '净资产收益率', '资产负债率']])

    current_year = pd.Timestamp.now().year
    recent_years = df_other[df_other['报告期'] >= (current_year - 6)]

    # print(recent_years.dtypes)
    # 计算平均值
    try:
        average_data = recent_years[['报告期', '每股净资产', '销售净利率', '销售毛利率', '净资产收益率', '资产负债率']]
    except Exception as e:
        continue

    # 将带有百分号的对象转换为小数
    try:
        for column in average_data.columns[1:]:  # 跳过报告期
            average_data[column] = average_data[column].str.replace('%', '').astype(float) / 100
    except Exception as e:
        continue

    print(type(average_data.mean()))

    # 将平均值添加到原 DataFrame
    print()
    for column in average_data.mean().index:
        print(column, average_data.mean()[column])
        filtered_df.loc[filtered_df['代码'] == code, column] = average_data.mean()[column]

    # print(filtered_df)
    # 保存更新后的 DataFrame 到 CSV 文件
    filtered_df.to_csv('test11.csv', index=False)
    # break

#
# # 输出结果
# print("近5年的平均数据:")
# print(average_data)