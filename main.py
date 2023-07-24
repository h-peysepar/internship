import pandas as pd
from tabulate import tabulate
from utility import calculate_columns, get_max_productivity, create_dataframe, get_expected_productivity
from scipy.optimize import minimize

df = create_dataframe()
df['Irrig. Scheduling F=10'] = df['IR']
calculate_columns(df)

def calculate_objective(df):
    product = df['Raes Method3'].product() 
    max = get_max_productivity()
    expected = get_expected_productivity()
    objective = expected - ((1 - product) * max)
    return objective

def objective_function(x, df):
    df['Irrig. Scheduling F=10'] = x
    calculate_columns(df)
    objective = calculate_objective(df)
    return abs(objective) 

def constraint(x, x_values, y_values):
    return y_values - x_values

result = minimize(objective_function, df['Irrig. Scheduling F=10'].values, args=(df,), constraints={'type': 'ineq', 'fun': constraint, 'args': (df['IR'].values, df['Irrig. Scheduling F=10'].values), }, bounds=[(0, None)])

optimized_y_values = result.x

df['Irrig. Scheduling F=10'] = optimized_y_values
calculate_columns(df)

optimized_objective = calculate_objective(df)

print("Optimized Objective Value:", optimized_objective)
print(df['Irrig. Scheduling F=10'].sum())





table = tabulate(df, headers=df.columns, tablefmt='outline')
print(table)
