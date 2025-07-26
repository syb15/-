import pandas as pd

df1 = pd.read_csv('boss.csv')

df2 = pd.read_csv('lp.csv')

df3 = pd.read_csv('qc.csv')

# 将三个DataFrame合并，这里使用concat函数按行方向（axis=0）合并
combined_df = pd.concat([df1, df2, df3], axis=0, ignore_index=True)

# 将合并后的数据保存为新的CSV文件，你可以根据需要修改文件名
combined_df.to_csv('ccc.csv', index=False)