import pandas as pd
from tabulate import tabulate

headers = ['Month', 'decade', 'progress level', 'Kc',
 'ETo', 'ETc', 'Pe', 'IR', 'Irrig. Scheduling F=10',]


df = pd.read_excel('data.xlsx', skiprows=102, nrows=23, usecols="A:I")
print(df)
df.columns = headers
df['Raes Method1'] = .5 * ( df['Irrig. Scheduling F=10'] / df['IR'])
df['Raes Method2'] = 1 - df['Raes Method1']
df['Raes Method3'] = pow(df['Raes Method2'], 10/220)
df['Raes Method4'] = 1 - df['Raes Method3']
df['Irrig. Scheduling F=30'] = None

for i in range(0, len(df), 3):
    df.loc[i, 'Irrig. Scheduling F=30'] = ''
    df.loc[i+2, 'Irrig. Scheduling F=30'] = ''
    df.loc[i+1, 'Irrig. Scheduling F=30'] = df.loc[i:i+2, 'Irrig. Scheduling F=10'].sum()



table = tabulate(df, headers=df.columns, tablefmt='outline')
print(table)
