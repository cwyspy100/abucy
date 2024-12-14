import os
import mysql.connector
from mysql.connector import Error
import pandas as pd
import time

# 数据库配置
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'wealth_data'

def create_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def insert_stock_data(connection, stock_name, insert_date, insert_price, moving_average, holding_days, price_change, deleted):
    cursor = connection.cursor()
    query = """
        INSERT INTO stock_data (stock_name, insert_date, insert_price, moving_average, holding_days, price_change, deleted)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (stock_name, insert_date, insert_price, moving_average, holding_days, price_change, deleted))
    connection.commit()
    cursor.close()

def update_stock_data(connection, stock_name, deleted_price, delete_date, holding_days, price_change, deleted):
    cursor = connection.cursor()
    query = """
        UPDATE stock_data
        SET deleted = %s, deleted_price = %s, deleted_date = %s, holding_days = %s, price_change = %s
        WHERE stock_name = %s AND deleted = 0
    """
    cursor.execute(query, (deleted, deleted_price, delete_date, holding_days, price_change, stock_name))
    connection.commit()
    cursor.close()

def process_stock_data(stock_name, stock_data):
    connection = create_connection()
    if connection is None:
        return

    for i in range(len(stock_data)):
        current_row = stock_data.iloc[i]
        current_price = current_row['close']
        moving_average = current_row['120_MA']
        current_date = current_row['date']

        if pd.isna(moving_average):
            continue  # 跳过均线数据尚未生成的行

        if current_price >= moving_average:
            # 检查数据库中是否已有未删除的记录
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM stock_data WHERE stock_name = %s AND deleted = 0", (stock_name,))
            existing_record = cursor.fetchone()
            cursor.close()

            if existing_record is None:
                # 如果没有未删除的记录，插入新记录
                insert_stock_data(connection, stock_name, current_date, current_price, moving_average, 1, 0, 0)
            else:
                if i == len(stock_data) - 1:
                    # 如果有未删除的记录，更新记录
                    insert_date = existing_record[2]  # 获取插入日期
                    insert_price = existing_record[3]  # 获取插入价格
                    holding_days = (current_date - insert_date).days  # 计算持有天数
                    price_change = (current_price - insert_price) / insert_price * 100
                    update_stock_data(connection, stock_name, current_price, current_date, holding_days, price_change, 0)

        elif current_price < moving_average:
            # 检查数据库中是否有未删除的记录
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM stock_data WHERE stock_name = %s AND deleted = 0", (stock_name,))
            existing_record = cursor.fetchone()
            cursor.close()

            if existing_record is not None:
                # 如果有未删除的记录，更新记录
                insert_date = existing_record[2]  # 获取插入日期
                insert_price = existing_record[3]  # 获取插入价格
                holding_days = (current_date - insert_date).days  # 计算持有天数
                price_change = (current_price - insert_price) / insert_price * 100
                update_stock_data(connection, stock_name, current_price, current_date, holding_days, price_change, 1)

    connection.close()


# 读取股票数据的函数
def read_stock_data(file_path):
    stock_data = None
    try:
        stock_data = pd.read_csv(file_path)
    except Exception as e:
        print("get stock data error {}".format(file_path))
    return stock_data

# 主程序
if __name__ == '__main__':
    folder_path = '/Users/water/abu/cn/stock/'  # 替换为您的文件夹路径
    start = time.time()

    # 遍历文件夹中的所有 CSV 文件
    for file_name in os.listdir(folder_path):
        print("hand file name {}".format(file_name))
        file_path = os.path.join(folder_path, file_name)
        stock_data = read_stock_data(file_path)
        if stock_data is None:
            continue
        # 将日期列设置为索引
        stock_data.set_index('date', drop=False, inplace=True)
        stock_data['date'] = pd.to_datetime(stock_data['date']).dt.date
        stock_data['120_MA'] = stock_data['close'].rolling(window=120).mean()

        # 从文件名提取股票代码
        stock_name = file_name.split('_')[0]  # 提取股票代码，例如 '001319'
        process_stock_data(stock_name, stock_data)

    print("数据处理完成！cost time {}".format(time.time() - start))