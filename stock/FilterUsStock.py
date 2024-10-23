# coding=utf-8


import pandas as pd
import chardet

# todo 美股获取
# 检测文件编码
def get_us_code():
    with open('20240424.csv', 'rb') as f:
        result = chardet.detect(f.read())
        print(result)

    # 使用检测到的编码读取文件
    df = pd.read_csv('20240424.csv')

    # 筛选总市值大于 100 亿的股票
    filtered_df = df[df['总市值'] > 100000000000]

    filtered_df = df[df['市盈率'] > 0]

    sorted_df = filtered_df.sort_values(by='市盈率')

    print(sorted_df[['序号', '名称', '总市值', '市盈率']].head(20))


#todo
# 使用检测到的编码读取文件
df = pd.read_csv('20240409.csv')

# 筛选总市值大于 100 亿的股票
filtered_df = df[
    (df['名称'].str.contains('银行') == False) &
    (df['总市值'] > 100000000000) &
    (df['市净率'] > 0 ) &
    (df['市净率'] <20)
    ]

sorted_df = filtered_df.sort_values(by='市净率')

print(sorted_df[['代码','名称','总市值', '市净率', '年初至今涨跌幅']].head(20))

# 计算过滤后的股票的涨幅之和
total_growth = sorted_df['年初至今涨跌幅'].head(20).sum()/100

# 输出结果
print(f"过滤后股票的涨幅之和: {total_growth:.2%}")
print(f"过滤后股票的平均涨幅: {(total_growth / 20):.2%}")