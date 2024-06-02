# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time


def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240531'):
    file_name = f"~/abu/cn/stock/{symbol}_{start_date}_{end_date}"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}

    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        # return pd.DataFrame()
        try:
            print('get data from file{}'.format(symbol))
            stock_data = ak.stock_zh_a_hist(symbol, period='daily', start_date=start_date, end_date=end_date, adjust="")
            stock_data = stock_data.rename(columns=column_names)
            selected_columns = stock_data.filter(items=column_names.values())
            selected_columns.to_csv(file_name, index=False)
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data


def get_stock_data():
    stock_data = ak.stock_zh_a_spot_em()
    return stock_data


def get_all_stock_data():
    """
        获取所有股票的数据
    """
    stock_data = pd.read_csv('20240409.csv')
    # 循环获取
    for i in stock_data['代码']:
        # 开头是8的股票代码，不处理
        code = f"{i:06}"
        if code[0] == '8':
            continue
        get_stock_data_by_name(code)
        # 休息10ms
        time.sleep(0.01)


def pick_stock(start_date='20230410', end_date='20240410'):
    stock_code_data = pd.read_csv('20240409.csv')
    choose_stock = []
    # 循环获取
    for i in stock_code_data['代码']:

        # 开头是8的股票代码，不处理
        code = f"{i:06}"
        if code[0] == '8':
            continue
        result1 = execute_strategy_mean(code, start_date, end_date)
        result2 = execute_strategy_volume(code, start_date, end_date)
        if result1 and result2:
            choose_stock.append(code)

    print("choose stock size:", len(choose_stock))
    print(f"选中的股票代码：{choose_stock}")
    # 将选中的股票代码写入文件
    with open(f"D:\\abu\\result\\choose_stock_{end_date}.txt", 'w') as f:
        for item in choose_stock:
            f.write(f"{item}\n")


def execute_strategy_mean(code, start_date='20230410', end_date='20240410'):
    """
    这是一个价格和120日均线的选股策略
    """
    try:
        stock_data = get_stock_data_by_name(code, start_date, end_date)

        if len(stock_data) < 120:
            return False

        # 计算120日均线
        stock_data['120日均线'] = stock_data['close'].rolling(window=120).mean()
        # 计算120均线最后一个数据
        last_120 = stock_data['120日均线'].iloc[-1]
        last_stock_close = stock_data['close'].iloc[-1]

        yesterday_120 = stock_data['120日均线'].iloc[-2]
        yesterday_last_stock_close = stock_data['close'].iloc[-2]

        if last_stock_close > last_120 and yesterday_120 > yesterday_last_stock_close:
            print(f"{code}股票价格{last_stock_close}大于120日均线{last_120}")
            return True
        return False
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} {code}")
        return False


def execute_strategy_volume(code, start_date='20230410', end_date='20240410'):
    """
    这是一个成家量的选股策略
    """
    try:
        stock_data = get_stock_data_by_name(code, start_date, end_date)

        if len(stock_data) < 120:
            return False

        last_stock_volume = stock_data['volume'].iloc[-1]
        yesterday_1 = stock_data['volume'].iloc[-2]
        yesterday_2 = stock_data['volume'].iloc[-3]
        yesterday_3 = stock_data['volume'].iloc[-4]
        yesterday_stock_volume = (yesterday_1 + yesterday_2 + yesterday_3) / 3

        # 价格筛选
        stock_data['120日均线'] = stock_data['close'].rolling(window=120).mean()
        # 计算120均线最后一个数据
        last_120 = stock_data['120日均线'].iloc[-1]
        last_stock_close = stock_data['close'].iloc[-1]

        if last_stock_volume > yesterday_stock_volume * 3 and last_stock_volume > yesterday_1 * 3 and last_stock_close > last_120:
            print(f"{code}股票价格{last_stock_close}大于120日成交量的3倍{yesterday_stock_volume * 3}")
            return True
        return False
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} {code}")
        return False


if __name__ == '__main__':
    """
    进行选股,主要测试通过价格和成交量选股
    """
    start_time = time.time()
    # pick_stock(end_date='20240415')
    get_all_stock_data()
    # get_stock_data_by_name("600519")
    end_time = time.time()
    print(f"耗时：{end_time - start_time}")
