import pandas as pd
from tabulate import tabulate
from utility import calculate_columns, get_max_productivity, create_dataframe, get_expected_productivity, get_efficiency
from scipy.optimize import minimize

df = create_dataframe()
# print(df)
df['Irrig. Scheduling F=10'] = df['IR']
calculate_columns(df)


# def calculate_objective(df):
#     max_productivity = get_max_productivity()  # 8333
#     expected_productivity = get_expected_productivity()  # 5000
#     efficiency = get_efficiency(df, max_productivity)  # 4999
#     error = expected_productivity - efficiency
#     print(error)
#     return error


# print(calculate_objective(df))
# # Extract the values from 'x' and 'y' columns
# x_values = df['IR'].values
# y_values = df['Irrig. Scheduling F=10'].values

# # Define the objective function and constraints


# def objective_function(x, df):
#     global x_values
#     global y_values
#     x_values = df['IR'].values
#     y_values = df['Irrig. Scheduling F=10'].values
#     calculate_columns(df)
#     error = calculate_objective(df)
#     # print(error)
#     return abs(error)


# def constraint(x, x_values, y_values):
#     return y_values - x_values  # Constraint: 'x' values <= 'y' values


# # Set the initial guess for optimization
# initial_guess = df['IR'].values

# # Perform the optimization
# result = minimize(objective_function, initial_guess, args=(df,), constraints={'type': 'ineq', 'fun': constraint, 'args': (x_values, y_values)})

# # Retrieve the optimized 'y' values
# print('x:', result.x)
# optimized_y_values = result.x

# # Update the DataFrame with the optimized 'y' values and calculate 'z'
# df['Irrig. Scheduling F=10'] = optimized_y_values
# calculate_columns(df)


# # Calculate the optimized objective value
# finalError = calculate_objective(df)

# # Print the optimized objective value and the updated DataFrame
# print("Optimized Objective Value:", finalError)
# print(df)



# Load the Excel file into a pandas DataFrame
# df = pd.read_excel('file.xlsx')

# Extract the values from 'IR' and 'Irrig. Scheduling F=10' columns
x_values = df['IR'].values
y_values = df['Irrig. Scheduling F=10'].values

# Define the objective function and constraints
def objective_function(x, df):
    df['Irrig. Scheduling F=10'] = x  # Update 'Irrig. Scheduling F=10' column with the optimization variable
    # df['Raes Method 3'] = df['Irrig. Scheduling F=10']**2  # Calculate 'Raes Method 3' based on the updated 'Irrig. Scheduling F=10' values
    calculate_columns(df)
    z_product = df['Raes Method3'].product()  # Product of 'Raes Method3' values
    objective = 5000 - ((1 - z_product) * 8333)  # Objective: O130 cell calculation
    return abs(objective)  # Objective: Minimize the absolute value of O130

def constraint(x, x_values, y_values):
    return y_values - x_values  # Constraint: 'IR' values <= 'Irrig. Scheduling F=10' values

# Set the initial guess for optimization
initial_guess = df['Irrig. Scheduling F=10'].values

# Perform the optimization
result = minimize(objective_function, initial_guess, args=(df,), constraints={'type': 'ineq', 'fun': constraint, 'args': (x_values, y_values), }, bounds=[(0, None)])

# Retrieve the optimized 'Irrig. Scheduling F=10' values
optimized_y_values = result.x

# Update the DataFrame with the optimized 'Irrig. Scheduling F=10' values and calculate 'Raes Method3'
df['Irrig. Scheduling F=10'] = optimized_y_values
calculate_columns(df)
# df['Raes Method3'] = df['Irrig. Scheduling F=10']**2

# Calculate the optimized objective value (O130 cell calculation)
z_product = df['Raes Method3'].product()
optimized_objective = 5000 - ((1 - z_product) * 8333)

# Print the optimized objective value and the updated DataFrame
print("Optimized Objective Value:", optimized_objective)
print(df['Irrig. Scheduling F=10'].sum())





table = tabulate(df, headers=df.columns, tablefmt='outline')
print(table)
