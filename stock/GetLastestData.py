# 获取市场的实时行情




import pandas as pd
import akshare as ak
from datetime import date
import os


# 1. 获取股票的实时行情
def pick_stock():
    current_date = date.today()
    file_name = "D:\\abu\\all\\{current_date}.csv"
    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        stock_data = ak.stock_zh_a_spot_em()
        stock_data.to_csv(file_name, index=False)
    return stock_data

    # stock_code_data = pd.read_csv('20240409.csv')
    # 循环获取
    # for i in stock_code_data['代码']:


def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = "D:\\abu\\stock\\{symbol}_{start_date}_{end_date}.csv"
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
            print("获取数据失败，错误信息：{e}")
            return pd.DataFrame()

    return stock_data


# 2. 将每个股票的实时行情保存到历史数据
def save_all_stock_data(stock_data):
    # 打印stock_data的股票代码
    print(stock_data['代码'])
    return stock_data






if __name__ == '__main__':
    current_date = date.today()
    stock_lastest_data = pick_stock()
    stock_lastest_data['代码'] = stock_lastest_data['代码'].astype(str)
    stock_data_300795 = stock_lastest_data[stock_lastest_data['代码'] == '688691']
    print(stock_data_300795)
    new_data = pd.DataFrame({'date': [current_date], 'open': [stock_data_300795['今开'][0]]
                             , 'close': [stock_data_300795['最新价'][0]], 'high': [stock_data_300795['最高'][0]]
                             , 'low': [stock_data_300795['最低'][0]], 'volume': [stock_data_300795['成交量'][0]]})
    print(type(stock_lastest_data))
    print(new_data.head())
    # print(stock_data_300795['今开'][0])
    

    stock_data = get_stock_data_by_name('000001')
    print(stock_data.head())
    # stock_data = stock_data.append(new_data)
    # stock_data.to_csv('688691.csv', ignore_index=True)

    # new_data = pd.DataFrame({'column1': ['value1'], 'column2': ['value2']})



    # for i in stock_lastest_data['代码']:
    #     # 开头是8的股票代码，不处理
    #     code = f"{i:06}"
    #     if code[0] == '8':
    #         continue
    #     stock_data = get_stock_data_by_name(code)
    #     # 增加一条数据
        
    #     stock_data.append(stock_data)



    # print(stock_data['代码'])