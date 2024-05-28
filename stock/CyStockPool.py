import akshare as ak
import time

import datetime

# 获取当前日期
today = datetime.date.today()

# 格式化成 '20240528'
today_str = today.strftime('%Y%m%d')
# # today_str = '20240527'
stock_zt_pool_strong_em_df = ak.stock_zt_pool_strong_em(date=today_str)
stock_zt_pool_strong_em_df.insert(1, '日期', today_str)
stock_zt_pool_strong_em_df.to_csv('../data/pool/strong_pool.csv', mode='a',  encoding='utf-8', index=False, header=False)


# stock_zt_pool_em_df = ak.stock_zt_pool_em(date='20240528')
# print(stock_zt_pool_em_df)


