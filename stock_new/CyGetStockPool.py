# -*- encoding: utf-8 -*-

import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime
import time

class StockPoolManager:
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
    
    def get_stock_daily_data(self):
        """获取股票日线数据，计算年度涨跌幅"""
        try:
            # 获取当年第一个交易日的数据
            current_year = datetime.now().year
            query_start = f"""
                SELECT 
                    sd.security_code,
                    si.security_name,
                    sd.close_price as year_start_price
                FROM stock_daily sd
                JOIN security_info si ON sd.security_code = si.security_code
                WHERE YEAR(sd.trade_date) = {current_year}
                AND sd.deleted = 0
                AND si.deleted = 0
                GROUP BY sd.security_code
                HAVING sd.trade_date = MIN(sd.trade_date)
            """
            year_start_data = pd.read_sql(query_start, self.engine)
            
            # 获取最新交易日的数据
            query_current = f"""
                SELECT 
                    sd.security_code,
                    sd.close_price as current_price,
                    sd.trade_date
                FROM stock_daily sd
                WHERE sd.deleted = 0
                GROUP BY sd.security_code
                HAVING sd.trade_date = MAX(sd.trade_date)
            """
            current_data = pd.read_sql(query_current, self.engine)
            
            # 合并数据并计算涨跌幅
            merged_data = pd.merge(year_start_data, current_data, on='security_code')
            merged_data['year_change_rate'] = (
                (merged_data['current_price'] - merged_data['year_start_price']) 
                / merged_data['year_start_price'] * 100
            ).round(2)
            
            # 筛选涨幅大于5%的股票
            filtered_data = merged_data[merged_data['year_change_rate'] > 5]
            
            # 添加时间戳
            current_time = datetime.now()
            filtered_data['created_at'] = current_time
            filtered_data['updated_at'] = current_time
            filtered_data['deleted'] = 0
            
            return filtered_data
        except Exception as e:
            print(f"获取股票数据失败: {str(e)}")
            return None
    
    def get_stock_data_by_date(self, end_date):
        """获取指定日期的股票数据，计算涨跌幅"""
        try:
            # 获取当年第一个交易日的数据
            year = end_date.year
            query_start = f"""
                SELECT 
                    sd.security_code,
                    si.security_name,
                    sd.close_price as year_start_price
                FROM stock_daily sd
                JOIN security_info si ON sd.security_code = si.security_code
                WHERE YEAR(sd.trade_date) = {year}
                AND sd.deleted = 0
                AND si.deleted = 0
                GROUP BY sd.security_code
                HAVING sd.trade_date = MIN(sd.trade_date)
            """
            year_start_data = pd.read_sql(query_start, self.engine)
            
            # 获取指定日期的数据
            query_current = f"""
                SELECT 
                    sd.security_code,
                    sd.close_price as current_price,
                    sd.trade_date
                FROM stock_daily sd
                WHERE sd.deleted = 0
                AND sd.trade_date <= '{end_date.strftime('%Y-%m-%d')}'
                GROUP BY sd.security_code
                HAVING sd.trade_date = MAX(sd.trade_date)
            """
            current_data = pd.read_sql(query_current, self.engine)
            
            # 合并数据并计算涨跌幅
            merged_data = pd.merge(year_start_data, current_data, on='security_code')
            merged_data['year_change_rate'] = (
                (merged_data['current_price'] - merged_data['year_start_price']) 
                / merged_data['year_start_price'] * 100
            ).round(2)
            
            # 筛选涨幅大于5%的股票
            filtered_data = merged_data[merged_data['year_change_rate'] > 5]
            
            # 添加时间戳
            current_time = datetime.now()
            filtered_data['created_at'] = current_time
            filtered_data['updated_at'] = current_time
            filtered_data['deleted'] = 0
            
            return filtered_data
        except Exception as e:
            print(f"获取股票数据失败: {str(e)}")
            return None
    
    def update_stock_pool(self, data):
        """更新股票池数据"""
        try:
            if data is not None and not data.empty:
                # 清空原有数据（软删除）
                update_query = "UPDATE stock_pool SET deleted = 1, updated_at = NOW() WHERE deleted = 0"
                with self.engine.connect() as conn:
                    conn.execute(update_query)
                
                # 插入新数据
                columns = [
                    'security_code', 'security_name', 'year_start_price',
                    'current_price', 'year_change_rate', 'created_at',
                    'updated_at', 'deleted'
                ]
                data[columns].to_sql(
                    'stock_pool',
                    self.engine,
                    if_exists='append',
                    index=False
                )
                print(f"成功更新股票池，共{len(data)}只股票")
            else:
                print("没有符合条件的股票数据")
        except Exception as e:
            print(f"更新股票池失败: {str(e)}")

def main():
    manager = StockPoolManager()
    stock_data = manager.get_stock_daily_data()
    manager.update_stock_pool(stock_data)

if __name__ == '__main__':
    main()