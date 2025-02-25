import akshare as ak
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
import time

class UpdateStockRealTimeData:
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
    
    def get_realtime_data(self):
        """获取实时行情数据"""
        try:
            # 使用akshare获取A股实时行情
            stock_data = ak.stock_zh_a_spot_em()
            if stock_data.empty:
                print("未获取到实时行情数据")
                return None
            
            # 格式化数据
            formatted_data = self._format_stock_data(stock_data)
            return formatted_data
        except Exception as e:
            print(f"获取实时行情数据失败: {str(e)}")
            return None
    
    def _format_stock_data(self, stock_data):
        """格式化股票数据"""
        try:
            # 选择需要的列并重命名
            required_columns = {
                '代码': 'security_code',
                '今开': 'open_price',
                '最新价': 'close_price',
                '最高': 'high_price',
                '最低': 'low_price',
                '成交量': 'volume',
                '成交额': 'amount',
                '涨跌幅': 'p_change'
            }
            
            formatted_data = stock_data[required_columns.keys()].copy()
            formatted_data.rename(columns=required_columns, inplace=True)
            
            # 添加日期和其他必要字段
            current_time = datetime.now()
            formatted_data['trade_date'] = current_time.date()
            formatted_data['created_at'] = current_time
            formatted_data['updated_at'] = current_time
            formatted_data['deleted'] = 0
            
            # 确保security_code是6位数字格式
            formatted_data['security_code'] = formatted_data['security_code'].str.zfill(6)
            
            return formatted_data
        except Exception as e:
            print(f"数据格式化失败: {str(e)}")
            return None
    
    def update_stock_data(self):
        """更新股票数据到数据库"""
        try:
            # 获取实时数据
            stock_data = self.get_realtime_data()
            if stock_data is None:
                return
            
            # 获取当前日期
            current_date = datetime.now().date()
            
            # 逐条处理数据
            success_count = 0
            skip_count = 0
            error_count = 0
            
            for _, row in stock_data.iterrows():
                try:
                    # 检查是否已存在
                    query = f"""SELECT id FROM stock_daily 
                              WHERE security_code = '{row['security_code']}' 
                              AND trade_date = '{current_date}' 
                              AND deleted = 0"""
                    existing = pd.read_sql(query, self.engine)
                    
                    if not existing.empty:
                        skip_count += 1
                        continue
                    
                    # 插入新数据
                    row_df = pd.DataFrame([row])
                    row_df.to_sql('stock_daily', self.engine, if_exists='append', index=False)
                    success_count += 1
                    
                except Exception as e:
                    print(f"处理股票 {row['security_code']} 数据时出错: {str(e)}")
                    error_count += 1
                    continue
            
            print(f"数据更新完成:\n成功: {success_count}\n跳过: {skip_count}\n错误: {error_count}")
            
        except Exception as e:
            print(f"更新数据过程中发生错误: {str(e)}")

if __name__ == '__main__':
    updater = UpdateStockRealTimeData()
    updater.update_stock_data()