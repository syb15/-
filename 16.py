import pandas as pd

# 读取CSV文件
data = pd.read_csv('ccc.csv')

# 基于整行去重，keep='first'表示保留第一次出现的重复行（可根据实际需求选'last'等）
data_unique = data.drop_duplicates(keep='last')

# 保存清洗后的数据为新的CSV文件，可按需修改文件名
data_unique.to_csv('ddd.csv', index=False)