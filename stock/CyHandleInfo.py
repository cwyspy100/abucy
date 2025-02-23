import pandas as pd

# 定义文件路径
xls_file_path = 'Table.xls'  # Excel 文件路径
csv_file_path = 'data.csv'   # CSV 文件路径
output_file_path = 'output.csv'  # 输出 CSV 文件路径

# 读取 Excel 文件
df_xls = pd.read_excel(xls_file_path)  # 假设包含“结束时间”和“名称”列

# 读取 CSV 文件
df_csv = pd.read_csv(csv_file_path)  # 假设包含“名称”，“细分行业”，“所属行业”，“上市日期”，“每股净资产”等列

# 过滤出结束时间为 2025-01-03 的数据
filtered_df = df_xls[df_xls['结束时间'] == '2025-01-03']

# 根据名称在两个 DataFrame 中进行合并
merged_df = pd.merge(filtered_df, df_csv, on='名称', how='inner')

# 选择所需的列
final_df = merged_df[['名称', '细分行业', '所属行业', '上市日期', '每股净资产']]

# 写入到新的 CSV 文件
final_df.to_csv(output_file_path, index=False)

print("数据处理完成，结果已写入到", output_file_path)