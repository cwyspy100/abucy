# 获取市场的实时行情


import pandas as pd
import akshare as ak
from datetime import date
import os
import  time
from util import RegUtil


# 1. 获取股票的实时行情
def get_all_latest_stock():
    current_date = date.today()
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"D:\\abu\\cn\\all\\{current_date}"
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
    file_name = f"D:\\abu\\cn\\all\\{current_date}"
    if os.path.exists(file_name):
        stock_data = pd.read_csv(file_name)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        print('get data from file error')
    return stock_data


def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"D:\\abu\\cn\\stock\\{symbol}_{start_date}_{end_date}"
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
def update_all_stock_data(start_date=20240410, end_date=20240412, single_end_data=20240412):
    """
    使用最新的实时数据来更新历史数据
    0、更新之前先备份一下数据
    1、start_date end_date 是全部最新数据文件
    2、更新获取最新数据

    """
    # start_date = 20240410
    # end_date = 20240412

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

            end = single_end_data
            if single_end_data > start_date:
                end = start_date

            stock_data = get_stock_data_by_name(code, cur_start_date, str(end))
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

            file_name = f"D:\\abu\\cn\\stock\\{code}_{cur_start_date}_{current_date}"
            stock_data.to_csv(file_name, index=False)

            # 删除文件，不删除文件可以进行每天测试
            # file_name = f"D:\\abu\\stock\\{code}_{cur_start_date}_{start_date}"
            # if os.path.exists(file_name):
            #     os.remove(file_name)
        start_date = i + 1


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
    for j in stock_latest_data['代码']:
        # 开头是8的股票代码，不处理
        code = f"{j:06}"
        if code[0] == '8':
            continue

        stock_data = get_stock_data_by_name(code, start_date, end_date)
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

        file_name = f"D:\\abu\\cn\\stock\\{code}_{start_date}_{all_stock_file_date}"
        stock_data.to_csv(file_name, index=False)

        # # 删除文件，不删除文件可以进行每天测试
        file_name = f"D:\\abu\\cn\\stock\\{code}_{start_date}_{end_date}"
        if os.path.exists(file_name):
            os.remove(file_name)


def pick_stock(start_date='20230410', end_date='20240410'):
    stock_code_data = pd.read_csv('20240409.csv')
    choose_stock_mean = []
    choose_stock_volume = []
    pick_result_df = pd.DataFrame(columns=['date', 'code', 'price', 'average', 'ang'])
    # 将 'code' 列的数据类型设置为 'object'
    pick_result_df['code'] = pick_result_df['code'].astype(str)

    # 循环获取
    for i in stock_code_data['代码']:

        # 开头是8的股票代码，不处理
        code = f"{i:06}"
        if code[0] == '8':
            continue
        stock_data = get_stock_data_by_name(code, start_date, end_date)
        result1 = execute_strategy_mean(stock_data, code)
        result2 = execute_strategy_ang(stock_data, 10, 'close')
        # result3 = execute_strategy_volume(stock_data, code, start_date, end_date)
        if result1 and result2 > 0:
        # if result3:
            choose_stock_mean.append(code)
            pick_result_df.loc[len(pick_result_df)] = [end_date, code, stock_data['close'].iloc[-1], result1, result2]

    pick_result_df.to_csv(f"D:\\abu\\cn\\result\\choose_stock_mean_ang.csv", mode='a', header=True, encoding='utf-8', index=False)

def pick_stock_new(start_date='20230410', end_date='20240410'):
    stock_code_data = pd.read_csv('20240409.csv')
    choose_stock_mean = []
    pick_result_df = pd.DataFrame(columns=['date', 'code', 'price', 'volumeang', 'closeang', 'rate'])
    # 将 'code' 列的数据类型设置为 'object'
    pick_result_df['code'] = pick_result_df['code'].astype(str)

    # 循环获取
    for i in stock_code_data['代码']:

        # 开头是8的股票代码，不处理
        code = f"{i:06}"
        if code[0] == '8':
            continue
        stock_data = get_stock_data_by_name(code, start_date, end_date)
        result1 = execute_strategy_ang(stock_data, 10, 'volume')
        result2 = execute_strategy_ang(stock_data, 10, 'close')
        if result1 > 5 and result2 > 5:
            choose_stock_mean.append(code)
            pick_result_df.loc[len(pick_result_df)] = [end_date, code, stock_data['close'].iloc[-1], result1, result2, result1/result2]

    pick_result_df.to_csv(f"D:\\abu\\cn\\result\\choose_stock_ang.csv", mode='a', header=True, encoding='utf-8', index=False)

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
        last_mean = stock_data['120日均线'].iloc[-1]
        last_stock_close = stock_data['close'].iloc[-1]

        yesterday_mean = stock_data['120日均线'].iloc[-2]
        yesterday_stock_close = stock_data['close'].iloc[-2]

        if last_stock_close > last_mean and yesterday_mean > yesterday_stock_close:
            print(f"{code}股票价格{last_stock_close}大于120日均线{last_mean}")
            return True
        return False
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} {code}")
        return False


def execute_strategy_volume(stock_data, code, start_date='20230410', end_date='20240410'):
    """
    这是一个成家量的选股策略
    """
    try:
        if stock_data is None:
            return False
        last_stock_volume = stock_data['volume'].iloc[-1]
        yesterday_1 = stock_data['volume'].iloc[-2]
        yesterday_2 = stock_data['volume'].iloc[-3]
        yesterday_3 = stock_data['volume'].iloc[-4]
        yesterday_stock_volume = (yesterday_1 + yesterday_2 + yesterday_3) / 3

        # 价格筛选
        if last_stock_volume > yesterday_stock_volume * 3 and last_stock_volume > yesterday_1 * 3:
            print(f"{code}股票价格{last_stock_volume}大于120日成交量的3倍{yesterday_stock_volume * 3}")
            return True
        return False
    except Exception as e:
        # print(f"获取数据失败，错误信息：{e} {code}")
        return False

def execute_strategy_ang(pd_stock_data, num, cloumeName):
    """
    这是一个成家量的选股策略
    """
    try:
        if len(pd_stock_data) < num:
            return False
        tmp = pd_stock_data[-num:]
        ang = RegUtil.calc_regress_deg(tmp[cloumeName], show=False)
        return ang
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} ")
        return 0



def test_ang(symbol, start_date='20230410', end_date='20240410'):
    pd_stock_data  = get_stock_data_by_name(symbol, start_date, end_date)
    if len(pd_stock_data) < 10:
        return False
    tmp = pd_stock_data[-10:]
    ang = RegUtil.calc_regress_deg(tmp['close'], show=False)
    print(ang)


"""
todo list
1、获取20240416的数据 get_all_latest_stock()
2、更新个单数据update_all_stock_data_simple("20230410", "20240415", "20240416")
3、选股，1，2,3 可以同时，但是 4  需要单独执行
"""
if __name__ == '__main__':
    start = time.time()
    current_date = 20240613
    # # 周一减少3天
    check_date = current_date - 1
    #
    # # 1、获取股票的实时行情
    # get_all_latest_stock()
    # # # # # # 2、将每个股票的实时行情保存到历史数据，更新多天有问题,只更新一天，周一需要单独设置两个时间
    # update_all_stock_data_simple("20230410", str(check_date), str(current_date))
    # # 3、对数据进行选股
    pick_stock(end_date=str(current_date))
    pick_stock_new(end_date=str(current_date))

    # 4、监控昨天选股情况
    # check_choose_stock_change(20240425, 20240426)

    test_ang('301176', end_date=str(current_date))

    # 4、回测股票
    print("time cost:", time.time() - start)

