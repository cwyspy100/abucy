# 获取市场的实时行情


import pandas as pd
import akshare as ak
from datetime import date
import os


# 1. 获取股票的实时行情
def pick_stock():
    current_date = date.today()
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"D:\\abu\\all\\{current_date}"
    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        stock_data = ak.stock_zh_a_spot_em()
        stock_data.to_csv(file_name, index=False)
    return stock_data


def pick_stock_by_date(current_date):
    global stock_data
    file_name = f"D:\\abu\\all\\{current_date}"
    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        print('get data from file error')
    return stock_data


def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"D:\\abu\\stock\\{symbol}_{start_date}_{end_date}"
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


# 2. 将每个股票的实时行情保存到历史数据
def update_all_stock_data():
    """
    使用最新的实时数据来更新历史数据
    0、更新之前先备份一下数据
    1、start_date end_date 是全部最新数据文件
    2、更新获取最新数据

    """
    start_date = 20240410
    end_date = 20240412

    # 循环start_date到end_date
    cur_start_date = '20230410'
    for i in range(start_date, end_date):
        current_date = str(i + 1)
        stock_latest_data = pick_stock_by_date(current_date)
        if stock_latest_data is None:
            continue

        # 将20240410 变为 2024-04-10
        save_current_date = f"{current_date[:4]}-{current_date[4:6]}-{current_date[6:]}"
        for j in stock_latest_data['代码']:
            # 开头是8的股票代码，不处理
            code = f"{j:06}"
            if code[0] == '8':
                continue
            stock_data = get_stock_data_by_name(code, cur_start_date, str(start_date))
            if stock_data is None or stock_data.size == 0:
                continue

            # 使用concat函数将新数据添加到现有的DataFrame中
            stock_new_data = stock_latest_data[stock_latest_data['代码'] == j]
            new_data = pd.DataFrame({'date': [save_current_date], 'open': [stock_new_data['今开'].iloc[0]]
                                        , 'close': [stock_new_data['最新价'].iloc[0]],
                                     'high': [stock_new_data['最高'].iloc[0]]
                                        , 'low': [stock_new_data['最低'].iloc[0]],
                                     'volume': [stock_new_data['成交量'].iloc[0]]})

            stock_data = pd.concat([stock_data, new_data], ignore_index=True)

            file_name = f"D:\\abu\\stock\\{code}_{cur_start_date}_{current_date}"
            stock_data.to_csv(file_name, index=False)

            # 删除文件，不删除文件可以进行每天测试
            # file_name = f"D:\\abu\\stock\\{code}_{cur_start_date}_{start_date}"
            # if os.path.exists(file_name):
            #     os.remove(file_name)
        start_date = i + 1


if __name__ == '__main__':
    # 1、获取股票的实时行情
    pick_stock()
    # 2、将每个股票的实时行情保存到历史数据
    update_all_stock_data()
    # 3、对数据进行选股
