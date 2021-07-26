import pandas as pd 

CSV_FILE = './data/Papers_data.csv'
CSV_FILE_1 = 'altmetrics.csv'

df1 = pd.read_csv(CSV_FILE,encoding='mac_roman')
df2 = pd.read_csv(CSV_FILE_1)

merged = df1.merge(df2, on="doi", how="outer").fillna("")
merged.to_csv("merged.csv", index=False)
