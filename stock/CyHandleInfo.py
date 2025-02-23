import pandas as pd

# �����ļ�·��
xls_file_path = 'Table.xls'  # Excel �ļ�·��
csv_file_path = 'data.csv'   # CSV �ļ�·��
output_file_path = 'output.csv'  # ��� CSV �ļ�·��

# ��ȡ Excel �ļ�
df_xls = pd.read_excel(xls_file_path)  # �������������ʱ�䡱�͡����ơ���

# ��ȡ CSV �ļ�
df_csv = pd.read_csv(csv_file_path)  # ������������ơ�����ϸ����ҵ������������ҵ�������������ڡ�����ÿ�ɾ��ʲ�������

# ���˳�����ʱ��Ϊ 2025-01-03 ������
filtered_df = df_xls[df_xls['����ʱ��'] == '2025-01-03']

# �������������� DataFrame �н��кϲ�
merged_df = pd.merge(filtered_df, df_csv, on='����', how='inner')

# ѡ���������
final_df = merged_df[['����', 'ϸ����ҵ', '������ҵ', '��������', 'ÿ�ɾ��ʲ�']]

# д�뵽�µ� CSV �ļ�
final_df.to_csv(output_file_path, index=False)

print("���ݴ�����ɣ������д�뵽", output_file_path)