import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime


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
    return datetime.datetime.strptime(datestr, '%Y-%m-%d').date()


def back_test(dfData , N):
    # 二八轮动：有空仓版
    df = dfData.copy()
    df['ret_300'] = df['hs300'].pct_change()
    df['ret_500'] = df['csi500'].pct_change()
    df['N_day_ret_300'] = df['hs300'] / df['hs300'].shift(N) - 1
    df['N_day_ret_500'] = df['csi500'] / df['csi500'].shift(N) - 1

    df['hs300_moving_average'] = df['hs300'].rolling(window=N).mean()
    df['hs500_moving_average'] = df['csi500'].rolling(window=N).mean()

    df['wgt_300'] = 0
    df['wgt_500'] = 0
    for i in range(1, len(df)):
        if i < N:
            continue
        t = df.index[i]
        t0 = df.index[i-1]
        if df.loc[t0, 'hs300'] >= df.loc[t0, 'hs300_moving_average']:
            df.loc[t, 'wgt_300'] = 1

        if df.loc[t0, 'csi500'] >= df.loc[t0, 'hs500_moving_average']:
            df.loc[t, 'wgt_500'] = 1

    # df['ret_stgy'] = df['ret_300'] * df['wgt_300'] + df['ret_500'] * df['wgt_500']
    df['ret_stgy'] = df['ret_500'] * df['wgt_500']
    df['ret_stgy_300'] = df['ret_300'] * df['wgt_300']
    # df['hs300_new'] = (1 + df['ret_300']).cumprod().fillna(1)
    # df['csi500_new'] = (1 + df['ret_500']).cumprod().fillna(1)
    df['stgy_500'] = (1 + df['ret_stgy']).cumprod().fillna(1)
    df['stgy_300'] = (1 + df['ret_stgy_300']).cumprod().fillna(1)

    fig = plt.figure(figsize=(20, 10))
    ax1 = fig.add_subplot(2, 1, 1)
    df.loc[:, ['hs300', 'csi500', 'stgy_500', 'stgy_300']].plot(ax=ax1, grid=True)
    plt.xlim(df.index[0], df.index[-1])


    ax2 = fig.add_subplot(2, 1, 2)
    df[['wgt_300', 'wgt_500']].plot(ax=ax2, kind='area', stacked=True, grid=True)
    plt.xlim(df.index[0], df.index[-1])
    plt.show()
    res = cal_period_perf_indicator(df.loc[:, ['hs300', 'csi500', 'stgy_500', 'stgy_300']])
    print("====================back_test {} ".format(N))
    print(res)

if __name__ == '__main__':
    index_price = pd.read_csv('date/300和500历史数据.csv').set_index('datetime')
    index_price.index = [datestr2dtdate(e) for e in index_price.index]
    # back_test(index_price, 1)
    # back_test(index_price, 5)
    # back_test(index_price, 10)
    back_test(index_price, 20)
    # back_test(index_price, 30)
    # back_test(index_price, 60)
    back_test(index_price, 90)
    back_test(index_price, 120)
    back_test(index_price, 250)