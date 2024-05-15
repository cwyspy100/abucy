
import os
import akshare as ak
import pandas as pd




def get_stock_data_by_name(symbol, start_date='20230410', end_date='20240410'):
    file_name = f"D:\\abu\\cn\\stock\\{symbol}_{start_date}_{end_date}"
    # column_names = {'日期': 'date', '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume'}

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


def pick_stock(start_date='20230410', end_date='20240410'):
    stock_code_data = pd.read_csv('20240409.csv')
    choose_stock_mean = []
    choose_stock_volume = []

    # 循环获取
    for i in stock_code_data['代码']:

        # 开头是8的股票代码，不处理
        code = f"{i:06}"
        if code[0] == '8':
            continue
        result,message = execute_plus_stock(code, start_date, end_date)
        if result:
            choose_stock_mean.append(message)

    with open(f"D:\\abu\\cn\\result\\choose_plus_stock_{end_date}", 'w', encoding="utf-8") as f:
        # f.write("--------------价格和120日均线选股策略\n")
        for item in choose_stock_mean:
            f.write(f"{item}\n")
        # f.write("---------------成交量选股策略\n")
        for item in choose_stock_volume:
            f.write(f"{item}\n")


def execute_plus_stock(code, start_date, end_date):
    stock_data = get_stock_data_by_name(code, start_date, end_date)
    if stock_data is None: # 读取文件失败
        return False, ""
    stock_data['change'] = stock_data['close'].pct_change(fill_method=None)
    # stock_data['change'].fillna(0, inplace=True)
    # df.method({col: value}, inplace=True)
    # stock_data.fillna({'change': 0}, inplace=True)

    # 统计大于0的数量
    up_num = stock_data[stock_data['change'] > 0].shape[0]
    total_num = stock_data['close'].shape[0]
    # print(up_num)
    annret = (stock_data['close'].iloc[-1] / stock_data['close'].iloc[0]) ** (242 / len(stock_data)) - 1  # 复利
    # if up_num / total_num > 0.5 or annret > 0.20:
    if annret > 0.20:
        return True, f"{code} is a plus stock  {up_num / total_num} annret {annret}"
    return False, ""






"""

主要是统计1年中涨幅大于0.2的股票 和对应年化收益率
"""
if __name__ == '__main__':
    pick_stock('20230410', '20240426')
