import akshare as ak
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime

class GetCurrentStockInfo:
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
    
    
    def fetch_current_market_data(self):
        """获取当前市场数据"""
        try:
            # 使用akshare获取A股实时行情数据
            df = ak.stock_zh_a_spot_em()
            # 打印数据长度
            print(f"获取到 {len(df)} 条股票数据")
            # 重命名列以匹配数据库表结构
            column_mapping = {
                '代码': 'code',
                '名称': 'name',
                '最新价': 'latest_price',
                '涨跌幅': 'change_percent',
                '涨跌额': 'change_amount',
                '成交量': 'volume',
                '成交额': 'amount',
                '振幅': 'amplitude',
                '最高': 'high_price',
                '最低': 'low_price',
                '今开': 'open_price',
                '昨收': 'pre_close',
                '量比': 'volume_ratio',
                '换手率': 'turnover_rate',
                '市盈率-动态': 'pe_ratio',
                '市净率': 'pb_ratio',
                '总市值': 'total_market_value',
                '流通市值': 'circulating_market_value',
                '涨速': 'change_speed',
                '5分钟涨跌': 'change_5min',
                '60日涨跌幅': 'change_60day',
                '年初至今涨跌幅': 'change_year'
            }
            
            df = df.rename(columns=column_mapping)
            # 添加交易日期
            df['trade_date'] = datetime.now().date()
            
            # 选择需要的列
            columns = ['trade_date', 'code', 'name', 'latest_price', 'change_percent', 'change_amount',
                      'volume', 'amount', 'amplitude', 'high_price', 'low_price', 'open_price',
                      'pre_close', 'volume_ratio', 'turnover_rate', 'pe_ratio', 'pb_ratio',
                      'total_market_value', 'circulating_market_value', 'change_speed',
                      'change_5min', 'change_60day', 'change_year']
            
            return df[columns]
        except Exception as e:
            print(f"获取市场数据失败: {str(e)}")
            return None
    
    def update_market_data(self):
        """更新市场数据"""
        try:
            # 获取当前市场数据
            market_data = self.fetch_current_market_data()
            if market_data is None or market_data.empty:
                print("没有获取到市场数据")
                return
            
            # 将数据写入数据库，如果存在则更新
            market_data.to_sql('market_daily', self.engine, if_exists='append', index=False,
                             method='multi', chunksize=1000)
            print(f"成功更新 {len(market_data)} 条市场数据")
            
        except Exception as e:
            print(f"更新市场数据失败: {str(e)}")

def main():
    collector = GetCurrentStockInfo()
    # 更新市场数据
    collector.update_market_data()

if __name__ == '__main__':
    main()