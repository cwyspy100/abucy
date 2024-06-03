# 获取市场的实时行情


import pandas as pd
import akshare as ak
from datetime import date
import os
import time
from util import RegUtil, PathUtil


# 1. 获取股票的实时行情
def get_all_latest_stock():
    current_date = date.today()
    current_date = current_date.strftime('%Y%m%d')
    file_name = f"abu/cn/all/{current_date}.csv"
    file_path = PathUtil.get_user_path(file_name)
    if os.path.exists(file_path):
        stock_data = pd.read_csv(file_path)
        # stock_data.rename(columns=column_names, inplace=True)
        print('get data from file')
    else:
        stock_data = ak.stock_zh_a_spot_em()
        stock_data.to_csv(file_path, index=False)
    return stock_data
# def pick_stock_by_date(current_date):
#     global stock_data
#     file_name = f"~/abu/cn/all/{current_date}"
#     if os.path.exists(file_name):
#         stock_data = pd.read_csv(file_name)
#         # stock_data.rename(columns=column_names, inplace=True)
#         print('get data from file')
#     else:
#         print('get data from file error')
#     return stock_data


def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"abu/cn/stock/{symbol}_{start_date}_{end_date}"
    column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}
    file_path = PathUtil.get_user_path(file_name)
    # print("file_name size : {}".format(os.path.getsize(file_name)))
    if os.path.exists(file_path) and os.path.getsize(file_path) > 2:
        try:
            stock_tmp_data = pd.read_csv(file_path)
            return stock_tmp_data
        except Exception as e:
            print(f"读取文件失败，错误信息：{e}")
            return None
    else:
        return None


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
        result1 = execute_strategy_mean_1(stock_data, start_date, end_date)
        result2 = execute_strategy_ang(stock_data, start_date, end_date)
        if result1 and result2 > 0:
            choose_stock_mean.append(code)
            pick_result_df.loc[len(pick_result_df)] = [end_date, code, stock_data['close'].iloc[-1], result1, result2]

    pick_result_df.to_csv(f"../todolist/choose_a_stock_bak.csv", mode='a', header=True, encoding='utf-8',
                          index=False)


def execute_strategy_mean(stock_data, code, start_date='20230410', end_date='20240410'):
    """
    这是一个价格和120日均线的选股策略
    """
    try:
        # stock_data = get_stock_data_by_name(code, start_date, end_date)

        if len(stock_data) < 60:
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


def execute_strategy_mean_1(stock_data, code, start_date='20230410', end_date='20240410'):
    """
    这是一个价格和120日均线的选股策略
    """
    try:
        # stock_data = get_stock_data_by_name(code, start_date, end_date)

        if len(stock_data) < 125:
            return False
        # 计算 120 日移动平均线
        stock_data['MA120'] = stock_data['close'].rolling(window=120).mean()
        # 获取最近 5 天的数据
        recent_6_days = stock_data.iloc[-6:]
        recent_5_days = stock_data.iloc[-5:]
        # 找出价格大于 120 日均线的数据
        # 检查每一天的价格是否大于当天的均线值
        start_condition = recent_6_days['MA120'].iloc[0] > recent_6_days['close'].iloc[0]
        all_above_MA120 = all(recent_5_days['close'] > recent_5_days['MA120'])
        if start_condition and all_above_MA120:
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


def execute_strategy_ang(pd_stock_data, code, start_date='20230410', end_date='20240410'):
    """
    这是一个成家量的选股策略
    """
    try:
        # pd_stock_data = get_stock_data_by_name(code, start_date, end_date)
        if len(pd_stock_data) < 10:
            return False
        tmp = pd_stock_data[-10:]
        ang = RegUtil.calc_regress_deg(tmp['close'], show=False)
        return ang
    except Exception as e:
        print(f"获取数据失败，错误信息：{e} {code}")
        return 0


def check_choose_stock_change(check_date, get_data_date):
    file_name = f"~/abu/cn/all/{get_data_date}"
    file_name_check = f"~/abu/cn/result/choose_stock_{check_date}"
    p_change = []
    stock_data = pd.read_csv(file_name)
    # 读取文件所有内容
    with open(file_name_check, 'r', encoding="utf-8") as f:
        # 读取文件所有内容
        # print(f.readlines())
        # print(type(f.readlines()))
        for i in f.readlines():
            # print(i.strip())
            # 从stock_data中找到对应的股票代码的涨跌幅
            stock_tmp_data = stock_data[stock_data['代码'] == int(i.strip())]
            # 获取涨跌幅的值
            # print("code {} : change {}".format(i.strip(), stock_tmp_data['涨跌幅'].iloc[0]))
            p_change.append("code {} : change {}".format(i.strip(), stock_tmp_data['涨跌幅'].iloc[0]))

    with open(f"~/abu/cn/result/choose_stock_{check_date}_pchange", 'w', encoding="utf-8") as f:
        # f.write("--------------价格和120日均线选股策略\n")
        for item in p_change:
            f.write(f"{item}\n")


"""
todo list
1、获取20240416的数据 get_all_latest_stock()
2、更新个单数据update_all_stock_data_simple("20230410", "20240415", "20240416")
3、选股，1，2,3 可以同时，但是 4  需要单独执行
"""
if __name__ == '__main__':
    start = time.time()
    current_date = 20240531
    # 周一减少3天
    check_date = current_date - 1

    # # # 1、获取股票的实时行情
    # get_all_latest_stock()
    # # # 2、将每个股票的实时行情保存到历史数据，更新多天有问题,只更新一天，周一需要单独设置两个时间
    # update_all_stock_data_simple("20230410", str(check_date), str(current_date))
    # 3、对数据进行选股
    pick_stock(end_date=str(current_date))

    # get_stock_data_by_name('301511', end_date=str(current_date))

    # 4、监控昨天选股情况
    # check_choose_stock_change(20240425, 20240426)

    # 4、回测股票
    print("time cost:", time.time() - start)
