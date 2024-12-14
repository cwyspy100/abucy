import mysql.connector
from mysql.connector import Error

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


def get_stock_data(stock_name):
    connection = create_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)  # 使用字典游标，便于访问列名
        try:
            query = "SELECT * FROM stock_data WHERE stock_name = %s AND deleted = 0"
            cursor.execute(query, (stock_name,))  # 使用参数化查询以防止 SQL 注入
            stock_data = cursor.fetchone()  # 获取第一条记录
            return stock_data
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()  # 关闭连接

# 使用示例
stock = get_stock_data('001319')
if stock:
    print(f"Stock Name: {stock['stock_name']}, Insert Price: {stock['insert_price']}, Insert Date: {stock['insert_date']}")
else:
    print("No active stock data found.")