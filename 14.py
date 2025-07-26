import pandas as pd

df1 = pd.read_csv('qc3.csv')

df2 = pd.read_csv('qc2.csv')

df3 = pd.read_csv('qc1.csv')

df4 = pd.read_csv('qc4.csv')

df5 = pd.read_csv('qc5.csv')

df6 = pd.read_csv('qc6.csv')

df7 = pd.read_csv('qc7.csv')

df8 = pd.read_csv('qc8.csv')

df9 = pd.read_csv('qc9.csv')

df10 = pd.read_csv('qc10.csv')

# 将三个DataFrame合并，这里使用concat函数按行方向（axis=0）合并
combined_df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], axis=0, ignore_index=True)

# 将合并后的数据保存为新的CSV文件，你可以根据需要修改文件名
combined_df.to_csv('qc.csv', index=False)