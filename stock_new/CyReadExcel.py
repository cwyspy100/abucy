import pandas as pd
import os

def read_excel_file():
    """读取Excel文件并返回DataFrame"""
    try:
        # 获取Excel文件的完整路径
        file_path = os.path.join(os.path.dirname(__file__), 'bbb.xlsx')
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"错误: 找不到文件 {file_path}")
            return None
            
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 显示数据基本信息
        print("\n数据基本信息:")
        print(df.info())
        
        # 显示前几行数据
        print("\n数据预览:")
        print(df.head())
        
        return df
    
    except Exception as e:
        print(f"读取Excel文件时出错: {str(e)}")
        return None

def main():
    df = read_excel_file()
    if df is not None:
        print("\nExcel文件读取成功！")

if __name__ == '__main__':
    main()