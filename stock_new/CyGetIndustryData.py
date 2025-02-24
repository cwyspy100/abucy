# -*- encoding: utf-8 -*-

import pandas as pd
import akshare as ak
from sqlalchemy import create_engine

# 数据库配置
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = 'localhost'
DB_NAME = 'wealth_data'

# 创建数据库连接
engine = create_engine(f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

def fetch_industry_data():
    # 获取申万一级行业数据
    sw_data = ak.sw_index_first_info()
    # 获取申万二级行业数据
    sw_second_data = ak.sw_index_second_info()
    
    # 处理一级行业数据
    l1_data = sw_data[['行业代码', '行业名称']].copy()
    l1_data.columns = ['industry_l1_code', 'industry_l1_name']
    l1_data['industry_l1_code'] = l1_data['industry_l1_code'].apply(lambda x: x.split('.')[0][-3:])
    
    # 处理二级行业数据
    l2_data = sw_second_data[['行业代码', '行业名称']].copy()
    l2_data.columns = ['industry_l2_code', 'industry_l2_name']
    l2_data['industry_l2_code'] = l2_data['industry_l2_code'].apply(lambda x: x.split('.')[0])
    l2_data['industry_l1_code'] = l2_data['industry_l2_code'].str[:3]
    
    # 打印处理后的数据
    print("\n处理后的一级行业数据：")
    print(l1_data)
    print("\n处理后的二级行业数据：")
    print(l2_data)
    
    # 合并一级和二级行业数据
    merged_data = pd.merge(l2_data, l1_data, on='industry_l1_code', how='inner')
    
    # 添加必要的字段
    merged_data['created_at'] = pd.Timestamp.now()
    merged_data['updated_at'] = pd.Timestamp.now()
    merged_data['deleted'] = 0
    
    return merged_data

def insert_industry_data(data):
    try:
        # 将数据插入到industry表
        data.to_sql('industry', con=engine, if_exists='append', index=False)
        print("行业数据插入成功！")
    except Exception as e:
        print(f"插入数据时发生错误：{str(e)}")

if __name__ == '__main__':
    # 获取行业数据
    industry_data = fetch_industry_data()
    
    # 打印最终数据
    print("\n最终合并的数据：")
    print(industry_data)
    
    # 插入数据到数据库
    insert_industry_data(industry_data)