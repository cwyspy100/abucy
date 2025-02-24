import pandas as pd
import os
from datetime import datetime
from sqlalchemy import create_engine

class SecurityInfoCollector:
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
    
    def get_security_info_from_excel(self):
        """从Excel文件获取证券基本信息"""
        try:
            # 读取Excel文件
            excel_path = os.path.join(os.path.dirname(__file__), 'bbb.xlsx')
            if not os.path.exists(excel_path):
                print(f"错误: 找不到文件 {excel_path}")
                return None
                
            try:
                stock_data = pd.read_excel(excel_path)
                if stock_data.empty:
                    print(f"警告: Excel文件 {excel_path} 是空的")
                    return None
                # 清理列名中的空格
                stock_data.columns = stock_data.columns.str.strip()
                print("Excel文件读取成功，显示所有列名：")
                print(stock_data.columns.tolist())
                print("\n数据预览：")
                print(stock_data.head())
                print("\n数据基本信息：")
                print(stock_data.info())
            except Exception as e:
                print(f"读取Excel文件时出错: {str(e)}")
                print(f"文件路径: {excel_path}")
                print(f"文件是否存在: {os.path.exists(excel_path)}")
                return None
            # 提取所需字段并重命名
            stock_info = pd.DataFrame()
            stock_info['security_code'] = stock_data['代码'].astype(str).str.strip().apply(lambda x: x.zfill(6))
            stock_info['security_name'] = stock_data['名称'].str.strip()
            stock_info['industry_1'] = stock_data['所属行业'].str.strip()
            stock_info['industry_2'] = stock_data['细分行业'].str.strip()
            stock_info['listing_date'] = stock_data['上市日期'].astype(str).str.strip()
            
            # 添加市场代码和证券类型
            stock_info['market_code'] = 'CN'
            stock_info['type_code'] = '01'  # 股票类型代码
            
            # 添加时间戳和删除标记
            current_time = datetime.now()
            stock_info['created_at'] = current_time
            stock_info['updated_at'] = current_time
            stock_info['deleted'] = 0
            
            # 数据清洗
            # 处理上市日期格式
            stock_info['listing_date'] = pd.to_datetime(
                stock_info['listing_date'], 
                format='%Y%m%d', 
                errors='coerce'
            ).dt.strftime('%Y-%m-%d')
            
            # 去除重复记录
            stock_info = stock_info.drop_duplicates(subset=['security_code'])
            
            return stock_info
        except Exception as e:
            print(f"处理股票数据时出错: {str(e)}")
            return None
    
    def save_to_db(self, data):
        """保存数据到数据库"""
        try:
            if data is not None and not data.empty:
                # 使用 DataFrame 的 to_sql 方法写入数据库
                data.to_sql(
                    'security_info',
                    self.engine,
                    if_exists='append',
                    index=False
                )
                print("数据成功写入数据库")
            else:
                print("没有数据需要写入")
        except Exception as e:
            print(f"写入数据库失败: {str(e)}")

def main():
    collector = SecurityInfoCollector()
    stock_info = collector.get_security_info_from_excel()
    collector.save_to_db(stock_info)

if __name__ == '__main__':
    main()