import pandas as pd
from tabulate import tabulate
from utility import calculate_columns, calculate_max_productivity, create_dataframe

df = create_dataframe()
df['Irrig. Scheduling F=10'] = df['IR']


calculate_columns(df)

table = tabulate(df, headers=df.columns, tablefmt='outline')
print(table)
