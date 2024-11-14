import akshare as ak
import time
import pandas as pd

from datetime import datetime
from util import PathUtil
import os

def get_file_path(dir_path):
    # 查询所有文件
    all_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            all_files.append(os.path.join(root, file))
            # 输出结果
    # for file in all_files:
    #     print(file)
    return all_files

def count_stock_keep(stock_path):
    # 读取股票数据
    try:
        df_data = pd.read_csv(stock_path)
    except Exception:
        return

    df = df_data.copy()
    # 确保日期列是日期时间格式
    df['date'] = pd.to_datetime(df['date'])
    # 使用 split 方法提取
    stock_code = stock_path.split('/')[-1].split('_')[0]
    # 按日期排序
    df.sort_values('date', inplace=True)

    # 计算 60 日均线
    df['60_MA'] = df['close'].rolling(window=60).mean()

    # 寻找 60日均线小于股价的时间段
    df['Condition'] = df['60_MA'] < df['close']

    # 识别条件变化的开始和结束
    df['Group'] = (df['Condition'] != df['Condition'].shift()).cumsum()

    # 找出满足条件的组
    groups = df[df['Condition']].groupby('Group')

    # 统计开始时间、结束时间和持续天数
    results = []

    for name, group in groups:
        start_date = group['date'].iloc[0]
        end_date = group['date'].iloc[-1]
        duration = (end_date - start_date).days + 1  # 包括结束当天
        # 计算涨跌幅
        start_price = group['close'].iloc[0]
        end_price = group['close'].iloc[-1]
        if start_price != 0:  # 防止除以零
            change_percent = ((end_price - start_price) / start_price)
            change_percent = round(change_percent, 2)
        else:
            change_percent = None

        results.append((stock_code, start_date.date(), end_date.date(), duration, change_percent))

    # 将结果转换为 DataFrame
    results_df = pd.DataFrame(results, columns=['code', '开始时间', '结束时间', '持续天数', '涨跌幅'])
    # 将结果写入 CSV 文件
    results_df.to_csv('results.csv', mode='a', header=False,  index=False, encoding='utf-8-sig')


    # 初始化计数器
    less_than_5_days = 0
    greater_than_5_days = 0
    total_change = 1

    # 统计持续天数
    for _, _, _, duration, change_percent in results:
        if duration < 5:
            less_than_5_days += 1
        else:
            greater_than_5_days += 1
        total_change *= (1+change_percent)
    # total_change = f"{total_change*100:.2f}%"

    radio = 0
    if (less_than_5_days > 0):
        radio = ((greater_than_5_days) / less_than_5_days)

    # 追加写入 CSV 文件
    summary_df = pd.DataFrame({
        '代码': [stock_code],
        '持续天数小于5': [less_than_5_days],
        '持续天数大于或等于5': [greater_than_5_days],
        '比率': [radio],
        # '总收益': [total_change]
        '总收益': [round((total_change-1), 2)]
    })

    # 将结果写入 CSV 文件
    summary_df.to_csv('results_summary.csv', mode='a', header=False, index=False, encoding='utf-8-sig')


def pick_stock_current_mean(stock_path, results = []):
    # 读取股票数据
    try:
        df = pd.read_csv(stock_path)
    except Exception:
        return

        # 确保日期列是日期时间格式
    df['date'] = pd.to_datetime(df['date'])

    stock_code = stock_path.split('/')[-1].split('_')[0]

    # 按日期排序
    df.sort_values('date', inplace=True)

    # 计算 60 日均线
    df['60_MA'] = df['close'].rolling(window=120).mean()

    # 寻找 60日均线小于股价的时间段
    df['Condition'] = df['60_MA'] < df['close']

    # 识别条件变化的开始和结束
    df['Group'] = (df['Condition'] != df['Condition'].shift()).cumsum()

    # 找出满足条件的组
    groups = df[df['Condition']].groupby('Group')

    # 统计开始时间、结束时间和持续天数
    # results = []

    # 获取最后一组的数据
    last_group_key = groups.groups.keys() # 使用 get_group 获取最后一组
    if len(last_group_key) == 0:
        return
    # print(list(last_group_key)[-1])
    last_group = groups.get_group(list(last_group_key)[-1])

    start_date = last_group['date'].iloc[0]
    end_date = last_group['date'].iloc[-1]
    duration = (end_date - start_date).days + 1  # 包括结束当天

    # 计算涨跌幅
    start_price = last_group['close'].iloc[0]
    end_price = last_group['close'].iloc[-1]
    if start_price != 0:  # 防止除以零
        change_percent = ((end_price - start_price) / start_price)
        # change_percent = f"{change_percent:.2f}%"  # 保留两位小数并加上 %
        change_percent = round((change_percent), 2)
    else:
        change_percent = None

    mean_change = change_percent / duration
    target_date = datetime.strptime('2024-06-14', '%Y-%m-%d').date()
    if end_date.date() == target_date:
        results.append((stock_code, start_date.date(), end_date.date(), duration, change_percent, mean_change))

    # 输出结果
    # for start, end, duration, change_percent in results:
    #     print(f"开始时间: {start}, 结束时间: {end}, 持续天数: {duration}天, 涨跌幅: {change_percent}")

    # # 将结果转换为 DataFrame
    # results_df = pd.DataFrame(results, columns=['code', '开始时间', '结束时间', '持续天数', '涨跌幅', '平均涨幅'])
    # # 将结果写入 CSV 文件
    # results_df.to_csv('results_monitor.csv', mode='a', header=False,  index=False, encoding='utf-8-sig')





if __name__ == '__main__':
    # 设置要查询的目录路径
    start = time.time()
    directory_path = '/Users/water/abu/cn/stock'
    all_files = get_file_path(directory_path)
    results = []
    for file in all_files:
        # print(file)
        # count_stock_keep(file)
        pick_stock_current_mean(file, results)

    # 将结果转换为 DataFrame
    results_df = pd.DataFrame(results, columns=['code', '开始时间', '结束时间', '持续天数', '涨跌幅', '平均涨幅'])
    # 将结果写入 CSV 文件
    results_df.to_csv('results_monitor.csv', mode='w', header=False,  index=False, encoding='utf-8-sig')

    print("execute cost time {}".format(time.time() - start))

    # pick_stock_current_mean('/Users/water/abu/cn/stock/603185_20230410_20240614')
    # count_stock_keep('/Users/water/abu/cn/stock/002930_20230410_20240614')