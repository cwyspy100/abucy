# 获取市场的实时行情


import pandas as pd
import akshare as ak
from datetime import date
import os
import time
from util import RegUtil


# 1. 获取股票的实时行情
def get_all_latest_stock():
    current_date = date.today()
    # 减少一天
    current_date = current_date.replace(day=current_date.day - 1)
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"D:\\abu\\us\\all\\{current_date}.csv"
    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        stock_data = ak.stock_us_spot_em()
        stock_data.to_csv(file_name, index=False)
    return stock_data


def pick_stock_by_date(current_date):
    file_name = f"D:\\abu\\us\\all\\{current_date}.csv"
    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
        return stock_data
    else:
        print('get data from file error')
    return None


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


def update_all_stock_data_simple(start_date='20240410', end_date='20240412', all_stock_file_date='20240415'):
    """
    使用最新的实时数据来更新历史数据，只更新一天
    start_date :end_date 是股票单个数据的时间
    all_stock_file_date 是全部最新数据文件的时间

    """
    stock_latest_data = pick_stock_by_date(all_stock_file_date)
    if stock_latest_data is None:
        return

    # 将20240410 变为 2024-04-10
    save_current_date = f"{all_stock_file_date[:4]}-{all_stock_file_date[4:6]}-{all_stock_file_date[6:]}"
    for code in stock_latest_data['代码']:
        # 开头是8的股票代码，不处理
        stock_data = get_stock_data_by_name(code, start_date, end_date)
        if stock_data is None or stock_data.size == 0:
            continue

        # 使用concat函数将新数据添加到现有的DataFrame中
        stock_new_data = stock_latest_data[stock_latest_data['代码'] == code]
        new_data = pd.DataFrame({'date': [save_current_date], 'open': [stock_new_data['开盘价'].iloc[0]]
                                    , 'close': [stock_new_data['最新价'].iloc[0]],
                                 'high': [stock_new_data['最高价'].iloc[0]]
                                    , 'low': [stock_new_data['最低价'].iloc[0]],
                                 'volume': [stock_new_data['成交量'].iloc[0]]})

        stock_data = pd.concat([stock_data, new_data], ignore_index=True)

        file_name = f"D:\\abu\\us\\stock\\{code}_{start_date}_{all_stock_file_date}"
        stock_data.to_csv(file_name, index=False)

        if end_date != all_stock_file_date:
            # 删除文件，不删除文件可以进行每天测试
            file_name = f"D:\\abu\\us\\stock\\{code}_{start_date}_{end_date}"
            if os.path.exists(file_name):
                os.remove(file_name)




def pick_stock(stock_code_data, start_date='20220101', end_date='20240410'):
    # stock_code_data = pd.read_csv('20240424.csv')
    choose_stock_mean = []
    choose_stock_volume = []
    pick_result_df = pd.DataFrame(columns=['date', 'code', 'price', 'average', 'ang', 'totalValue'])
    # 将 'code' 列的数据类型设置为 'object'
    pick_result_df['code'] = pick_result_df['code'].astype(str)

    # 循环获取
    for code in stock_code_data['代码']:
        new_pirce = stock_code_data.loc[stock_code_data['代码'] == code, '最新价'].values[0]
        total_value = stock_code_data.loc[stock_code_data['代码'] == code, '总市值'].values[0]
        # 价格大于2 小于 500 ，市值大于10亿
        if new_pirce < 2 or new_pirce > 500 or total_value < 1000000000:
            continue
        stock_data = get_stock_data_by_name(code, start_date, end_date)
        result1 = execute_strategy_mean(stock_data, code)
        result2 = execute_strategy_ang(stock_data, 10, 'close')
        if result1 and result2 > 5:
            choose_stock_mean.append(code)
            pick_result_df.loc[len(pick_result_df)] = [end_date, code, stock_data['close'].iloc[-1], result1, result2, total_value]

    pick_result_df.to_csv(f"D:\\abu\\us\\result\\choose_us_stock.csv", mode='a', header=True, encoding='utf-8', index=False)
    # pick_result_df.to_csv(f"D:\\abu\\us\\result\\choose_us_stock_{end_date}.csv", mode='w', header=True,
    #                       encoding='utf-8',
    #                       index=False)


def pick_stock_ang(stock_code_data, start_date='20220101', end_date='20240410'):
    # stock_code_data = pd.read_csv('20240424.csv')
    choose_stock_mean = []
    choose_stock_volume = []
    pick_result_df = pd.DataFrame(columns=['date', 'code', 'price', 'volumeang', 'priceang', 'totalValue'])
    # 将 'code' 列的数据类型设置为 'object'
    pick_result_df['code'] = pick_result_df['code'].astype(str)

    # 循环获取
    for code in stock_code_data['代码']:
        new_pirce = stock_code_data.loc[stock_code_data['代码'] == code, '最新价'].values[0]
        total_value = stock_code_data.loc[stock_code_data['代码'] == code, '总市值'].values[0]
        if new_pirce < 2 or new_pirce > 500 or total_value < 1000000000:
            continue
        stock_data = get_stock_data_by_name(code, start_date, end_date)
        result1 = execute_strategy_ang(stock_data, 60, 'volume')
        result2 = execute_strategy_ang(stock_data, 60, 'close')
        if result1 > 5  and result2 > 5:
            choose_stock_mean.append(code)
            pick_result_df.loc[len(pick_result_df)] = [end_date, code, stock_data['close'].iloc[-1], result1, result2, total_value]

    pick_result_df.to_csv(f"D:\\abu\\us\\result\\choose_us_stock_ang.csv", mode='w', header=True, encoding='utf-8', index=False)



def execute_strategy_ang(pd_stock_data, num, label):
    """
    这是一个成家量的选股策略
    """
    try:
        # pd_stock_data = get_stock_data_by_name(code, start_date, end_date)
        if len(pd_stock_data) < num:
            return False
        tmp = pd_stock_data[-num:]
        ang = RegUtil.calc_regress_deg(tmp[label], show=False)
        return ang
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} ")
        return 0


def execute_strategy_mean(stock_data, code):
    """
    这是一个价格和120日均线的选股策略
    """
    try:
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



def check_choose_stock_change(get_data_date):
    stock_latest_data = pick_stock_by_date(get_data_date)
    if stock_latest_data is None:
        print("当前数据是空，请确认")
        return
    check_path = f"D:\\abu\\us\\result\\choose_us_stock.csv"
    check_pd = pd.read_csv(check_path)
    if check_pd is None:
        print("确认数据是空，请确认")
        return
    # 初始化第一天的价格变化为0
    check_pd['latest_price'] = 0.0
    check_pd['p_change'] = 0.0
    check_pd['value'] = 0.0

    # check_pd['code'] = check_pd['code'].str.replace('"', '')
    for j in check_pd['code']:
        # 从stock_prices数据框中获取该股票的最新价格

        if j == 'code':
            continue
        latest_data = stock_latest_data.loc[stock_latest_data['代码'] == j]
        if latest_data is None or len(latest_data) == 0:
            continue

        latest_price = latest_data['最新价'].values[0]
        latest_value = latest_data['总市值'].values[0]

        # 从stock_history数据框中获取该股票的历史价格
        historical_price = float(check_pd.loc[check_pd['code'] == j, 'price'].values[0])
        value = float(check_pd.loc[check_pd['code'] == j, 'price'].values[0])

        # 计算价格变化率
        price_change = round((latest_price - historical_price) / historical_price * 100, 2)

        check_pd.loc[check_pd['code'] == j, 'latest_price'] = latest_price
        check_pd.loc[check_pd['code'] == j, 'p_change'] = price_change
        check_pd.loc[check_pd['code'] == j, 'value'] = latest_value

    check_pd.to_csv(f"D:\\abu\\us\\result\\choose_us_stock.csv"
                    , mode='w', header=True, encoding='utf-8',
                    index=False)




def check_code_mean_ang(symbol, start_date, end_date , set_start, set_end ):
    """
    测试当时选择是否正确
    set_start,set_end 设定时间范围
    """
    pd_stock_data = get_stock_data_by_name(symbol, start_date, end_date)
    if pd_stock_data is None:
        return

    stock_data = pd_stock_data.loc[(pd_stock_data['date'] >= set_start) & (pd_stock_data['date'] <= set_end)]
    result1 = execute_strategy_mean(stock_data, symbol)
    result2 = execute_strategy_ang(stock_data, 10, 'volume')
    result3 = execute_strategy_ang(stock_data, 10, 'close')
    print("mean :{} ang {} result3 {}".format(result1, result2, result3))

"""
todo list
1、获取20240416的数据 get_all_latest_stock()
2、更新个单数据update_all_stock_data_simple("20230410", "20240415", "20240416")
3、选股，1，2,3 可以同时，但是 4  需要单独执行
"""
if __name__ == '__main__':
    start = time.time()
    current_date = 20241212
    check_date = current_date - 1
    # check_date = 20241025
    #
    # # # 1、获取股票的实时行情
    stock_data = get_all_latest_stock()
    # # # # # 2、将每个股票的实时行情保存到历史数据，更新多天有问题
    update_all_stock_data_simple("20220101", str(check_date), str(current_date))
    # # # # # # # 3、对数据进行选股
    pick_stock(stock_data, end_date=str(current_date))
    pick_stock_ang(stock_data, end_date=str(current_date))
    #
    # # 4、监控昨天选股情况
    check_choose_stock_change(current_date)

    # check_code_mean_ang('105.SLRX', '20230410', '20240619', '2023-04-10', '2023-06-19')

    # 4、回测股票
    print("time cost:", time.time() - start)

