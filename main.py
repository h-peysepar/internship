import pandas as pd
from tabulate import tabulate
from utility import calculate_columns, get_max_productivity, create_dataframe, get_expected_productivity,get_efficiency
from scipy.optimize import minimize

df = create_dataframe()
# print(df)
df['Irrig. Scheduling F=10'] = df['IR']
calculate_columns(df)

def calculate_objective(df): 
  max_productivity = get_max_productivity() # 8333
  expected_productivity = get_expected_productivity() # 5000
  efficiency = get_efficiency(df, max_productivity) # 4999
  error = expected_productivity - efficiency
  print(error)
  return error

print(calculate_objective(df))
# Extract the values from 'x' and 'y' columns
x_values = df['IR'].values
y_values = df['Irrig. Scheduling F=10'].values

# Define the objective function and constraints
def objective_function(x, df):
    calculate_columns(df)
    error = calculate_objective(df)
    # print(error)
    return abs(error)

def constraint(x, x_values, y_values):
    return y_values - x_values  # Constraint: 'x' values <= 'y' values

# Set the initial guess for optimization
initial_guess = df['IR'].values

# Perform the optimization
result = minimize(objective_function, initial_guess, args=(df,), constraints={'type': 'ineq', 'fun': constraint, 'args': (x_values, y_values)})

# Retrieve the optimized 'y' values
optimized_y_values = result.x

# Update the DataFrame with the optimized 'y' values and calculate 'z'
df['Irrig. Scheduling F=10'] = optimized_y_values
calculate_columns(df)


# Calculate the optimized objective value
finalError = calculate_objective(df)

# Print the optimized objective value and the updated DataFrame
print("Optimized Objective Value:", finalError)
print(df)



table = tabulate(df, headers=df.columns, tablefmt='outline')
print(table)
