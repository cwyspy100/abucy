import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

class CyMonitorStockPool:
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
    
    def get_stock_data(self, start_date, end_date):
        """获取指定时间段的股票数据，计算涨跌幅"""
        try:
            # 获取初始日期的数据
            query_start = f"""
                SELECT 
                    sd.security_code,
                    si.security_name,
                    sd.close_price as start_price,
                    sd.trade_date
                FROM stock_daily sd
                JOIN security_info si ON sd.security_code = si.security_code
                WHERE sd.trade_date = '{start_date}'
                AND sd.deleted = 0
                AND si.deleted = 0
            """
            start_data = pd.read_sql(query_start, self.engine)
            
            # 获取结束日期的数据
            query_end = f"""
                SELECT 
                    sd.security_code,
                    sd.close_price as current_price,
                    sd.trade_date
                FROM stock_daily sd
                WHERE sd.trade_date = '{end_date}'
                AND sd.deleted = 0
            """
            end_data = pd.read_sql(query_end, self.engine)
            
            # 合并数据并计算涨跌幅
            merged_data = pd.merge(start_data, end_data, on='security_code')
            merged_data['change_rate'] = (
                (merged_data['current_price'] - merged_data['start_price']) 
                / merged_data['start_price'] * 100
            ).round(2)
            
            # 筛选涨幅大于5%的股票
            filtered_data = merged_data[merged_data['change_rate'] > 5].copy()
            
            # 添加时间戳
            current_time = datetime.now()
            filtered_data.loc[:, 'created_at'] = current_time
            filtered_data.loc[:, 'updated_at'] = current_time
            filtered_data.loc[:, 'deleted'] = 0
            
            # 重命名列以匹配stock_pool表结构
            filtered_data = filtered_data.rename(columns={
                'start_price': 'year_start_price',
                'current_price': 'current_price',
                'change_rate': 'year_change_rate'
            })
            
            return filtered_data
        except Exception as e:
            print(f"获取股票数据失败: {str(e)}")
            return None
    
    def update_stock_pool(self, data):
        """更新股票池数据"""
        try:
            if data is not None and not data.empty:
                # 清空原有数据（软删除）
                from sqlalchemy import text
                update_query = text("UPDATE stock_pool SET deleted = 1, updated_at = NOW() WHERE deleted = 0")
                
                # 使用事务进行更新
                with self.engine.begin() as conn:
                    # 执行软删除
                    conn.execute(update_query)
                    
                    # 插入新数据
                    columns = [
                        'security_code', 'security_name', 'year_start_price',
                        'current_price', 'year_change_rate', 'created_at',
                        'updated_at', 'deleted'
                    ]
                    data[columns].to_sql(
                        'stock_pool',
                        conn,
                        if_exists='append',
                        index=False
                    )
                print(f"成功更新股票池，共{len(data)}只股票")
            else:
                print("没有符合条件的股票数据")
        except Exception as e:
            print(f"更新股票池失败: {str(e)}")
    
    def monitor_stock_pool(self, start_date, end_date):
        """监控股票池主函数"""
        try:
            # 获取股票数据并计算涨跌幅
            stock_data = self.get_stock_data(start_date, end_date)
            
            # 更新股票池
            self.update_stock_pool(stock_data)
            
            print(f"股票池监控完成，监控期间：{start_date} 至 {end_date}")
        except Exception as e:
            print(f"股票池监控失败: {str(e)}")

# 使用示例
if __name__ == '__main__':
    monitor = CyMonitorStockPool()
    start_date = '2025-01-02'  # 初始时间
    end_date = '2025-02-21'    # 当前时间
    monitor.monitor_stock_pool(start_date, end_date)