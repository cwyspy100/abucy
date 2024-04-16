# -*- encoding =utf8 -*-

"""
想法如下：
1、获得一个股票的数据
2、对数据进行回测
3、选股策略是选定股票
4、买入策略当前close的价格大于120日均线价格买入
5、卖出策略是当前close的价格小于120日均线卖出，或者从收益最大算收益跌幅5%
6、计算参数

"""

import pandas as pd
import akshare as ak
import os
import numpy as np
import matplotlib.pyplot as plt
import mplfinance as mpf


def get_drawdown(p):
    """
    计算净值回撤
    """
    T = len(p)
    hmax = [p[0]]
    for t in range(1, T):
        hmax.append(np.nanmax([p[t], hmax[t - 1]]))
    dd = [p[t] / hmax[t] - 1 for t in range(T)]

    return dd


def cal_period_perf_indicator(adjnav):
    """
    计算区间业绩指标:输入必须是日频净值
    年化收益率、年化波动率、夏普比率、最大回撤和卡玛比率
    'AnnRet', 'AnnVol', 'SR', 'MaxDD', 'Calmar'
    """

    if type(adjnav) == pd.DataFrame:
        res = pd.DataFrame(index=adjnav.columns, columns=['AnnRet', 'AnnVol', 'SR', 'MaxDD', 'Calmar'])
        for col in adjnav:
            res.loc[col] = cal_period_perf_indicator(adjnav[col])

        return res

    ret = adjnav.pct_change()
    # annret = np.nanmean(ret) * 242 # 单利
    annret = (adjnav.iloc[-1] / adjnav.iloc[0]) ** (242 / len(adjnav)) - 1  # 复利
    annvol = np.nanstd(ret) * np.sqrt(242)
    sr = annret / annvol
    dd = get_drawdown(adjnav)
    mdd = np.nanmin(dd)
    calmar = annret / -mdd

    return [annret, annvol, sr, mdd, calmar]


def get_stock_data(symbol, start_date='20170301', end_date='20240321'):
    file_name = f"../data/stock/{symbol}_{start_date}_{end_date}.csv"
    column_names = {'日期': 'day', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low'}

    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        stock_data.rename(columns=column_names, inplace=True)
    else:
        try:
            stock_data = ak.stock_zh_a_hist(symbol, period='daily', start_date=start_date, end_date=end_date, adjust="")
            stock_data.rename(columns=column_names, inplace=True)
            stock_data.to_csv(file_name, index=False)
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data


def pick_stock():
    pass


def buy_strategy_mean():
    pass


def sell_stategy_mean():
    pass


def back_test_stock(symbol):
    """
    此方法，针对股票回测的年化收益很高，同时移动均线时间越短，越高，有问题，思考一下原因？？？
    当天计算的均线，当天买入，有问题
    df['hold'] = np.where(df['close'] > df['moving_average'], 1, 0)

    :param symbol:
    :return:
    """
    stock_data = get_stock_data(symbol)
    df = stock_data.copy()
    # 计算120日均线
    df['moving_average'] = df['close'].rolling(window=120).mean()

    # 创建一个新的列来跟踪是否持有股票
    df['hold'] = np.where(df['close'] > df['moving_average'], 1, 0)

    # 创建一个新的列来跟踪每次买入后的累计收益
    df['stock_change'] = df['close'].pct_change()
    df['cumulative_return'] = df['hold'] * df['stock_change']

    # 创建一个新的列来跟踪每次买入后的最大累计收益
    df['max_cumulative_return'] = df.groupby((df['hold'] == 0).cumsum()).cumulative_return.cummax()

    # 创建一个新的列来计算回撤
    df['drawdown'] = df['cumulative_return'] - df['max_cumulative_return']

    # 如果回撤小于或等于-5%，则卖出股票
    df.loc[df['drawdown'] <= -0.05, 'hold'] = 0

    df['action'] = 'hold'  # 默认操作是'hold'
    df.loc[(df['hold'] == 1) & (df['hold'].shift() == 0), 'action'] = 'buy'
    df.loc[(df['hold'] == 0) & (df['hold'].shift() == 1), 'action'] = 'sell'

    # 假设df是你的DataFrame，'action'是买卖点，'day'是日期
    buy_sell_df = df.loc[df['action'].isin(['buy', 'sell']), ['day', 'action', 'close']]

    # 按日期排序
    buy_sell_df = buy_sell_df.sort_values('day')

    # 重置索引
    buy_sell_df = buy_sell_df.reset_index(drop=True)
    print(buy_sell_df)

    df['result_strategy'] = df['stock_change'] * df['hold']
    df['total_strategy'] = (1 + df['result_strategy']).cumprod().fillna(1)
    res = cal_period_perf_indicator(df.loc[:, ['close', 'total_strategy']])
    print(res)


def back_test_mean_new():
    pass


if __name__ == '__main__':
    # back_test_stock('600519')

    stock_data = get_stock_data('600519')
    # 对股票按照index循环
    N = 120
    df = stock_data.copy()
    df['stock_change'] = df['close'].pct_change()
    df['stock_keep'] = 0
    df['stock_moving_average'] = df['close'].rolling(window=N).mean()

    # 找到持有的数据
    for i in range(1, len(df)):
        if i < N:
            continue
        t = df.index[i]
        t0 = df.index[i - 1]
        if df.loc[t0, 'close'] >= df.loc[t0, 'stock_moving_average']:
            df.loc[t, 'stock_keep'] = 1

    df['result_strategy'] = df['stock_change'] * df['stock_keep']
    df['total_strategy'] = (1 + df['result_strategy']).cumprod().fillna(1)

    # 创建一个新的列 max_total_strategy 来跟踪到目前为止的最大累计收益。
    # 创建一个新的列 drawdown 来计算当前累计收益与最大累计收益之间的差异。
    # 如果 drawdown 小于或等于 -5%，那么就不持有
    df['max_total_strategy'] = df['total_strategy'].cummax()
    df['drawdown'] = (df['total_strategy'] / df['max_total_strategy']) - 1

    # 如果 drawdown 小于或等于 -5%，那么就不持有
    df.loc[df['drawdown'] <= -0.05, 'stock_keep'] = 0
    df['result_strategy'] = df['stock_change'] * df['stock_keep']
    df['total_strategy'] = (1 + df['result_strategy']).cumprod().fillna(1)

    df['action'] = 'hold'  # 默认操作是'hold'
    df.loc[(df['stock_keep'] == 1) & (df['stock_keep'].shift() == 0), 'action'] = 'buy'
    df.loc[(df['stock_keep'] == 0) & (df['stock_keep'].shift() == 1), 'action'] = 'sell'

    # 假设df是你的DataFrame，'action'是买卖点，'day'是日期
    buy_sell_df = df.loc[df['action'].isin(['buy', 'sell']), ['day', 'action', 'close']]

    # 按日期排序
    buy_sell_df = buy_sell_df.sort_values('day')

    # 重置索引
    buy_sell_df = buy_sell_df.reset_index(drop=True)
    print(buy_sell_df)

    res = cal_period_perf_indicator(df.loc[:, ['close', 'total_strategy']])
    print(res)
