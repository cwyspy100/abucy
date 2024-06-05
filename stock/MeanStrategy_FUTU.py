import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import os


def get_drawdown(p):
    """
    计算净值回撤
    """
    T = len(p)
    hmax = [p.iloc[0]]
    for t in range(1, T):
        hmax.append(np.nanmax([p.iloc[t], hmax[t - 1]]))
    dd = [p.iloc[t] / hmax[t] - 1 for t in range(T)]

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
    annret = (adjnav.iloc[-1] / adjnav.iloc[0]) ** (242 / len(adjnav)) - 1  # 复利
    annvol = np.nanstd(ret) * np.sqrt(242)
    sr = annret / annvol
    dd = get_drawdown(adjnav)
    mdd = np.nanmin(dd)
    calmar = annret / -mdd

    return [annret, annvol, sr, mdd, calmar]


def datestr2dtdate(datestr):
    # 日期格式转换：'yyyy-mm-dd'转为datetime.date
    return datetime.datetime.strptime(datestr, '%Y-%m-%d').date()


def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"D:\\abu\\us\\stock\\{symbol}_{start_date}_{end_date}"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}

    # print("file_name size : {}".format(os.path.getsize(file_name)))
    if os.path.exists(file_name) and os.path.getsize(file_name) > 2:
        try:
            stock_tmp_data = pd.read_csv(file_name)
            return stock_tmp_data
        except Exception as e:
            print(f"读取文件失败，错误信息：{e}")
            return None
    else:
        return None



def back_test(dfData , N):
    # 二八轮动：有空仓版
    df = dfData.copy()
    df['ret_300'] = df['open'].pct_change()
    df['hs300_moving_average'] = df['open'].rolling(window=N).mean()

    df['wgt_300'] = 0
    df['wgt_300_cost'] = 0.01
    for i in range(1, len(df)):
        if i < N:
            continue
        t = df.index[i]
        t0 = df.index[i-1]
        if df.loc[t0, 'open'] >= df.loc[t0, 'hs300_moving_average']:
            df.loc[t0, 'wgt_300'] = 1

        # if df.loc[t0, 'csi500'] >= df.loc[t0, 'hs500_moving_average']:
        #     df.loc[t, 'wgt_500'] = 1

    df['ret_stgy_300'] = (df['ret_300'] - df['wgt_300_cost']) * df['wgt_300']
    df['stgy_300'] = (1 + df['ret_stgy_300']).cumprod().fillna(1)

    res = cal_period_perf_indicator(df.loc[:, ['open', 'stgy_300']])
    print("====================back_test {} ".format(N))
    print(res)

if __name__ == '__main__':
    # index_price = pd.read_csv('date/300和500历史数据.csv').set_index('datetime')
    # index_price.index = [datestr2dtdate(e) for e in index_price.index]
    index_price = get_stock_data_by_name("105.FUTU", "20230410", "20240530").set_index('date').loc[:, ['open']]
    # index_price = get_stock_data_by_name("105.GOOG", "20230410", "20240528").set_index('date').loc[:, ['open']]
    # index_price = get_stock_data_by_name("106.BABA", "20230410", "20240528").set_index('date').loc[:, ['open']]
    index_price.index = [datestr2dtdate(e) for e in index_price.index]

    # back_test(index_price, 1)
    back_test(index_price, 5)
    # back_test(index_price, 10)
    # back_test(index_price, 20)
    # back_test(index_price, 30)
    # back_test(index_price, 60)
    # back_test(index_price, 90)
    # back_test(index_price, 120)
    # back_test(index_price, 250)