import pandas as pd

df = pd.read_csv("../resources/standard_stats_5.csv")
print(df[df['Player']=='Lionel Messi']['Player'])
print(df.loc[0]['Player'])
print(df.columns)

item = 'PK'

print(max(df[item]), min(df[item]))

item = 'Min'

print(max(df[item]), min(df[item]))

item = 'MP'

print(max(df[item]), min(df[item]))