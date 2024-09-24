import akshare as ak
import time
import pandas as pd

import datetime

# 获取当前日期
today = datetime.date.today()

# 格式化成 '20240528'
# today_str = today.strftime('%Y%m%d')
# # # today_str = '20240527'
# stock_zt_pool_strong_em_df = ak.stock_zt_pool_strong_em(date=today_str)
# stock_zt_pool_strong_em_df.insert(1, '日期', today_str)
# stock_zt_pool_strong_em_df.to_csv('../data/pool/strong_pool.csv', mode='a',  encoding='utf-8', index=False, header=False)


# stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20240528')
# print(stock_zt_pool_em_df)


# 过滤掉代码开头是8的，市值需要大于100亿，将市盈率小于15的过滤出来
# 读取 CSV 文件
csv_file_path = '20240924.csv'  # 替换为你的 CSV 文件路径
data = pd.read_csv(csv_file_path, dtype={'代码': str})
print(data.info())

# # 过滤条件
# # 1. 股票代码开头不是 '8'
# # 2. 市值大于 100 亿
# # 3. 市盈率小于 15
# filtered_data = data[
#     ~(data['代码'].str.startswith('8')) &  # 股票代码开头不是 '8'
#     (data['总市值'] > 100000000000) &                      # 市值大于 100 亿 (假设市值单位为亿)
#     (data['市盈率-动态'] < 15) &                     # 市盈率小于 15
#     (data['市盈率-动态'] > 0)
#     ]
#
# # print(filtered_data.size)
# sorted_data = filtered_data.sort_values(by='市盈率-动态')
# # 输出过滤后的数据
# print(sorted_data[['序号', '代码', '名称', '总市值', '市盈率-动态', '年初至今涨跌幅']])



# filtered_data = data[
#     ~(data['代码'].str.startswith('8')) &  # 股票代码开头不是 '8'
#     (data['总市值'] > 100000000000) &                      # 市值大于 100 亿 (假设市值单位为亿)
#     (data['市净率'] < 15) &                     # 市盈率小于 15
#     (data['市净率'] > 0)
#     ]
#
# print(filtered_data.size)
# sorted_data = filtered_data.sort_values(by='市净率')
# # 输出过滤后的数据
# print(sorted_data[['序号', '代码', '名称', '总市值', '市盈率-动态', '市净率', '年初至今涨跌幅']])


# filtered_data = data[
#     ~(data['代码'].str.startswith('8')) &  # 股票代码开头不是 '8'
#     (data['总市值'] > 100000000000)  #&                      # 市值大于 100 亿 (假设市值单位为亿)
#     # (data['市净率'] < 15) &                     # 市盈率小于 15
#     # (data['市净率'] > 0)
#     ]
#
# print(filtered_data.size)
# sorted_data = filtered_data.sort_values(by='年初至今涨跌幅', ascending=False)
# # 输出过滤后的数据
# print(sorted_data[['序号', '代码', '名称', '总市值', '市盈率-动态', '市净率', '年初至今涨跌幅']].head(20))


# stock_data = ak.stock_zh_a_spot_em()
# stock_data.to_csv('20240924.csv')


# sorted_data = data.sort_values(by='成交额', ascending=False)
# # 输出过滤后的数据
# print(sorted_data[['序号', '代码', '名称', '总市值', '市盈率-动态', '市净率', '年初至今涨跌幅', '涨跌幅', '成交额']].head(30))



# 计算总成交额，80%都到了那些股票

total_turnover = data['成交额'].sum()
print(data['成交额'].sum())
# 按成交额排序
sorted_data = data.sort_values(by='成交额', ascending=False)

# 计算累积成交额
sorted_data['累积成交额'] = sorted_data['成交额'].cumsum()

# 计算 80% 的阈值
threshold = total_turnover * 0.8

# 找到累积成交额达到 80% 的股票
contributing_stocks = sorted_data[sorted_data['累积成交额'] <= threshold]

# 打印结果
print("达到总成交额 80% 的股票：")
print(contributing_stocks[['代码','名称', '成交额','涨跌幅', '累积成交额']])
