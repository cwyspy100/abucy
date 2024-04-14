# 获取一个股票的数据
import akshare as ak
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os


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
    """

    if type(adjnav) == pd.DataFrame:
        res = pd.DataFrame(index=adjnav.columns, columns=['AnnRet', 'AnnVol', 'SR', 'MaxDD', 'Calmar'])
        for col in adjnav:
            res.loc[col] = cal_period_perf_indicator(adjnav[col])

        return res

    ret = adjnav.pct_change()
    # annret = np.nanmean(ret) * 242 # 单利
    annret = (adjnav[-1] / adjnav[0]) ** (242 / len(adjnav)) - 1  # 复利
    annvol = np.nanstd(ret) * np.sqrt(242)
    sr = annret / annvol
    dd = get_drawdown(adjnav)
    mdd = np.nanmin(dd)
    calmar = annret / -mdd

    return [annret, annvol, sr, mdd, calmar]


def datestr2dtdate(datestr):
    # 日期格式转换：'yyyy-mm-dd'转为datetime.date
    if isinstance(datestr, str):
        return datetime.datetime.strptime(datestr, '%Y-%m-%d').date()
    else:
        return datestr


# def get_stock_data_by_name(symbol, start_date='20170301', end_date='20240321'):
#     file_name = symbol+'_'+start_date+'_'+end_date+'.csv'
#     stock_data = pd.DataFrame()
#     try:
#         stock_data = pd.read_csv(file_name)
#         # 重命名列名
#         stock_data = stock_data.rename(columns={'日期': 'day', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low'})
#     except FileNotFoundError:
#         print("文件不存在或路径错误。请检查文件路径和文件名。")

#     # 判断stock_data 是空
#     if stock_data.empty:
#         stock_data = ak.stock_zh_a_hist(symbol, period='daily', start_date=start_date, end_date=end_date, adjust="" )
#         stock_data.to_csv(file_name)
#         stock_data = pd.read_csv(file_name)
#         stock_data = stock_data.rename(columns={'日期': 'day', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low'})
#     # print(stock_data.tail())
#     return stock_data

def get_stock_data_by_name(symbol, start_date='20170301', end_date='20240321'):
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


def back_test(dfData, N):
    # 二八轮动：有空仓版
    df = dfData.copy()
    df['ret_300'] = df['close'].pct_change()
    # df['N_day_ret_500'] = df['csi500'] / df['csi500'].shift(N) - 1

    df['hs300_moving_average'] = df['close'].rolling(window=N).mean()

    df['wgt_300'] = 0
    # df['wgt_500'] = 0
    for i in range(1, len(df)):
        if i < N:
            continue
        t = df.index[i]
        t0 = df.index[i]
        if df.loc[t0, 'close'] >= df.loc[t0, 'hs300_moving_average']:
            df.loc[t, 'wgt_300'] = 1
    df['ret_stgy_300'] = df['ret_300'] * df['wgt_300']
    df['stgy_300'] = (1 + df['ret_stgy_300']).cumprod().fillna(1)

    res = cal_period_perf_indicator(df.loc[:, ['close', 'stgy_300']])
    print("====================back_test {} ".format(N))
    print(res)

    # 归一化
    df['close_norm'] = (df['close'] - df['close'].min()) / (df['close'].max() - df['close'].min())
    df['stgy_300_norm'] = (df['stgy_300'] - df['stgy_300'].min()) / (df['stgy_300'].max() - df['stgy_300'].min())
    # 画图
    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(2, 1, 1)
    df.loc[:, ['close_norm', 'stgy_300_norm']].plot(ax=ax1, grid=True)
    plt.xlim(df.index[0], df.index[-1])

    ax2 = fig.add_subplot(2, 1, 2)
    df[['wgt_300']].plot(ax=ax2, kind='area', stacked=True, grid=True)
    plt.xlim(df.index[0], df.index[-1])
    plt.legend()
    plt.show()


def back_test_open(dfData, N):
    # 二八轮动：有空仓版
    df = dfData.copy()
    df['ret_300'] = df['open'].pct_change()
    # df['N_day_ret_500'] = df['csi500'] / df['csi500'].shift(N) - 1

    df['hs300_moving_average'] = df['open'].rolling(window=N).mean()

    df['wgt_300'] = 0
    # df['wgt_500'] = 0
    for i in range(1, len(df)):
        if i < N:
            continue
        t = df.index[i]
        t0 = df.index[i]
        if df.loc[t0, 'open'] >= df.loc[t0, 'hs300_moving_average']:
            df.loc[t, 'wgt_300'] = 1
    df['ret_stgy_300'] = df['ret_300'] * df['wgt_300']
    df['stgy_300'] = (1 + df['ret_stgy_300']).cumprod().fillna(1)

    res = cal_period_perf_indicator(df.loc[:, ['open', 'stgy_300']])
    print("====================back_test {} ".format(N))
    print(res)

    # 归一化
    # df['close_norm'] = (df['open'] - df['open'].min()) / (df['open'].max() - df['open'].min())
    # df['stgy_300_norm'] = (df['stgy_300'] - df['stgy_300'].min()) / (df['stgy_300'].max() - df['stgy_300'].min())
    # # 画图
    # fig = plt.figure(figsize=(20, 10))
    # ax1 = fig.add_subplot(2, 1, 1)
    # df.loc[:, ['open_norm', 'stgy_300_norm']].plot(ax=ax1, grid=True)
    # plt.xlim(df.index[0], df.index[-1])
    #
    # ax2 = fig.add_subplot(2, 1, 2)
    # df[['wgt_300']].plot(ax=ax2, kind='area', stacked=True, grid=True)
    # plt.xlim(df.index[0], df.index[-1])
    # plt.legend()
    # plt.show()


def back_test_new(N=5):
    stock_data = get_stock_data_by_name('600519').set_index('day')
    stock_data.index = [datestr2dtdate(e) for e in stock_data.index]
    back_test(stock_data, N)
    back_test_open(stock_data, N)


if __name__ == '__main__':
    # back_test_new()
    # back_test_new(10)
    back_test_new(20)
    # back_test_new(30)
    # back_test_new(60)
    back_test_new(120)
    # back_test_new(240)
    # stock_zh_a_hist_df = ak.stock_zh_a_hist(symbol="000001", period="daily", start_date="20170301", end_date='20240321', adjust="")
    # print(stock_data.tail())
    # back_test(stock_data, 5)
