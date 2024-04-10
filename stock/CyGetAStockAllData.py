# -*- encoding: utf-8 -*-

import akshare as ak
import pandas as pd
import os
import time

def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"D:\\abu\\stock\\{symbol}_{start_date}_{end_date}.csv"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}

    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        # print('get data from file')
    else:
        try:
            stock_data = ak.stock_zh_a_hist(symbol, period='daily', start_date=start_date, end_date=end_date, adjust="")
            stock_data = stock_data.rename(columns=column_names)
            selected_columns = stock_data.filter(items=column_names.values())
            selected_columns.to_csv(file_name, index=False)
        except Exception as e:
            print(f"获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data


def get_stock_data():
    stock_data =  ak.stock_zh_a_spot_em()
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


def pick_stock():
    stock_code_data = pd.read_csv('20240409.csv')
    choose_stock = []   
    # 循环获取
    for i in stock_code_data['代码']:
        
        # 开头是8的股票代码，不处理
        code = f"{i:06}"
        if code[0] == '8':
            continue
        result = execute_stratgy(code)
        if result:
            choose_stock.append(code)

    print("choose stock size:", len(choose_stock))  
    print(f"选中的股票代码：{choose_stock}")


def execute_stratgy(code):
    try:
        stock_data = get_stock_data_by_name(code)
        # 计算120日均线
        stock_data['120日均线'] = stock_data['close'].rolling(window=120).mean()
        # 计算120均线最后一个数据
        last_120 = stock_data['120日均线'].iloc[-1]
        last_stock_close = stock_data['close'].iloc[-1]

        yesterday_120 = stock_data['120日均线'].iloc[-2]
        yesterday_last_stock_close = stock_data['close'].iloc[-2]   

        # if last_120 > yesterday_120 and last_stock_close < yesterday_last_stock_close:
        #     print(f"{code}股票价格{last_stock_close}小于120日均线{last_120}")
        #     return False

        # if yesterday_120 > yesterday_last_stock_close:
        #     print(f"{code}昨天股票价格{yesterday_last_stock_close}小于120日均线{yesterday_120}")
        #     return False

        vaule = last_120 * 0.1
        if last_stock_close > last_120 and last_stock_close - last_120 < vaule and yesterday_120 > yesterday_last_stock_close:
            print(f"{code}股票价格{last_stock_close}大于120日均线{last_120}")
            return True
        return False
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} {code}")
        return False






if __name__ == '__main__':
    # get_stock_data()
    # stock_data =  ak.stock_zh_a_spot_em()
    # print(stock_data)
    # stock_data.to_csv('20240409.csv', index=False) 
    
    # 保存数字的时候，前面的0被省略了，需要补全
    # stock_data = get_stock_data_by_name('300795')
    # print(stock_data.tail(10))

    start_time = time.time()
    pick_stock()
    end_time = time.time()
    print(f"耗时：{end_time - start_time}")
 
