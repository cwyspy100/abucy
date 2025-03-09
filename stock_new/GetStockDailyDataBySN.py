# -*- encoding: utf-8 -*-

import pandas as pd
import akshare as ak
from sqlalchemy import create_engine
from datetime import datetime, timedelta
import time

class GetStockDailyData:
    def __init__(self):
        # 数据库配置
        self.DB_USER = 'root'
        self.DB_PASSWORD = 'root'
        self.DB_HOST = 'localhost'
        self.DB_NAME = 'wealth_data'
        
        # 创建数据库连接
        self.engine = create_engine(
            f'mysql+mysqlconnector://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}'
        )
    
    def get_stock_codes(self):
        """从security_info表获取股票代码列表"""
        try:
            query = "SELECT security_code FROM security_info WHERE deleted = 0"
            stock_codes = pd.read_sql(query, self.engine)
            return stock_codes['security_code'].tolist()
        except Exception as e:
            print(f"获取股票代码列表失败: {str(e)}")
            return []
    
    def fetch_stock_data(self, stock_code):
        """获取单个股票的历史数据"""
        try:
            # 计算两年前的日期
            end_date = datetime.now()
            start_date = end_date - timedelta(days=200)
            
            # 使用akshare获取股票数据
            # 获取股票代码的后六位
            # stock_code = stock_code[-6:]
            print(f"正在获取股票 {stock_code} 的数据...")
            stock_data = ak.stock_zh_a_daily(
                symbol=stock_code,
                start_date=start_date.strftime('%Y%m%d'),
                end_date=end_date.strftime('%Y%m%d'),
                adjust=""
            )
            
            if stock_data.empty:
                print(f"股票 {stock_code} 没有数据")
                return None
            
            # 直接选择需要的列
            required_columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'amount']
            try:
                stock_data = stock_data[required_columns]
            except KeyError as e:
                print(f"错误：缺少必要的数据列 {e}，无法继续处理")
                return None
            
            # 重命名列
            column_mapping = {
                'date': 'trade_date',
                'open': 'open_price',
                'close': 'close_price',
                'high': 'high_price',
                'low': 'low_price',
                'volume': 'volume',
                'amount': 'amount'
            }
            stock_data = stock_data.rename(columns=column_mapping)
            
            # 添加股票代码和时间戳
            tmp_stock_code = stock_code[-6:]
            stock_data['security_code'] = tmp_stock_code
            stock_data['created_at'] = datetime.now()
            stock_data['updated_at'] = datetime.now()
            stock_data['p_change'] = 0
            stock_data['deleted'] = 0
            
            # 确保日期格式正确
            stock_data['trade_date'] = pd.to_datetime(stock_data['trade_date']).dt.date
            
            # print(stock_data.head())
            return stock_data
        except Exception as e:
            print(f"获取股票 {stock_code} 的数据失败: {str(e)}")
            return None
    
    def save_stock_data(self, data):
        """保存股票数据到数据库"""
        try:
            if data is not None and not data.empty:
                # 选择需要保存的列
                columns_to_save = [
                    'trade_date', 'security_code', 'open_price', 'close_price', 'high_price', 'low_price',
                    'volume', 'amount', 'p_change', 'created_at', 'updated_at', 'deleted'
                ]
                data[columns_to_save].to_sql(
                    'stock_daily',
                    self.engine,
                    if_exists='append',
                    index=False
                )
                print(f"股票 {stock_code} 的数据保存成功")
            else:
                print("没有数据需要保存")
        except Exception as e:
            print(f"保存数据失败: {str(e)}")


    def check_and_update_stock_data(self):
        """检查并更新股票数据"""
        stock_codes = self.get_stock_codes()
        total_stocks = len(stock_codes)
        print(f"共找到 {total_stocks} 只股票需要检查和更新")

        for i, stock_code in enumerate(stock_codes, 1):
            print(f"正在检查和更新第 {i}/{total_stocks} 只股票: {stock_code}")
            tmp_stock_code = stock_code[-6:]
            # 获取数据库中已有的数据
            query = f"""SELECT trade_date FROM stock_daily
                      WHERE security_code = '{tmp_stock_code}'
                      AND trade_date = '2025-03-07'
                      AND deleted = 0
                      ORDER BY trade_date DESC
                      LIMIT 1"""
            existing_data = pd.read_sql(query, self.engine)
            if not existing_data.empty:
                print(f"股票 {stock_code} 的数据无需更新")
            else:
                # 将股票代码前两位转为小写
                stock_code = stock_code[:2].lower() + stock_code[2:]
                print(f"股票 {stock_code} 没有数据，需要获取")
                stock_data = self.fetch_stock_data(stock_code)
                self.save_stock_data(stock_data)
                # 添加延时避免请求过于频繁
                time.sleep(1)

def main():
    collector = GetStockDailyData()
    collector.check_and_update_stock_data()
    # stock_data = collector.fetch_stock_data('sz300002')
    print(stock_data.head())

if __name__ == '__main__':
    main()