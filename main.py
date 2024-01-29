import pandas as pd
from tabulate import tabulate
from math import prod
from scipy.optimize import minimize
from config import read_config

inputSheet = pd.read_excel(
    'data.xlsx', sheet_name='Input', skiprows=1, nrows=5, usecols="A:B")
cropHistory = pd.read_excel(
    'data.xlsx', sheet_name='Crop History', skiprows=1, nrows=9, usecols="B:B")


def get_expected_productivity():
    expected = read_config('EXPECTED_CROP_YEILD')
    sws = read_config('SOIL_WATER_SOLINITY')
    age = read_config('AGE')
    if sws and sws > 7:
        expected = 100 - 3.6 * (expected - 7)
    if(age):
        if(age < 3):
            expected *= .4
        elif age < 6:
            expected *= .7
        elif age < 9:
            expected *= .9
    return expected


def create_dataframe(inputData):
    df = pd.DataFrame(inputData)
    return df


def calculate_columns(df):
    df['Raes Method1'] = df['Progress Stage'] * \
        (df['Irrigation Scheduling'] / df['Irrigation'])
    df['Raes Method2'] = 1 - df['Raes Method1']
    df['Raes Method3'] = pow(df['Raes Method2'], 10/220)
    df['Raes Method4'] = 1 - df['Raes Method3']
    # cycle = read_config('IRRIGATION_FREQUENCY')
    # cycle_key = f'Irrigation Scheduling F={cycle}'
    # df[cycle_key] = None
    # jump = cycle / 10
    # for i in range(0, len(df)):
    #     if (i % jump) == 0:
    #         sum = df.loc[i: i + jump - 1, 'Irrigation Scheduling'].sum()
    #         capacity = read_config('FIELD_CAPACITY')
    #         df.loc[i, cycle_key] = sum if capacity > sum else capacity


temp = {
    'Progress Stage': [.5],
    'Kc': [.38],
    'ETo': [40.74],
    'ETc': [12.19],
    'Effective Precipitation': [2.36],
    'Irrigation': [9.83],
}


def optimizer(inputdata):
    df = create_dataframe(inputdata)
    df['Irrigation Scheduling'] = df['Irrigation']
    calculate_columns(df)
    # print(df)

    def calculate_objective(df):
        product = df['Raes Method3'].product()
        max = read_config("MAX_CROP_EFFICIENCY")
        expected = get_expected_productivity()
        objective = expected - ((1 - product) * max)
        return objective

    def objective_function(x, df):
        df['Irrigation Scheduling'] = x
        calculate_columns(df)
        print(df['Irrigation Scheduling'][0])

        objective = calculate_objective(df)
        return abs(objective)

    def constraint(x, x_values, y_values):
        return y_values - x_values

    result = minimize(objective_function, df['Irrigation Scheduling'].values, args=(df,), constraints={
                      'type': 'ineq', 'fun': constraint, 'args': (df['Irrigation'].values, df['Irrigation Scheduling'].values), }, bounds=[(0, None)])

    optimized_y_values = result.x

    df['Irrigation Scheduling'] = optimized_y_values
    calculate_columns(df)

    optimized_objective = calculate_objective(df)

    print("Optimized Objective Value:", optimized_objective)
    print("Total Irrigation Water: ", df['Irrigation Scheduling'].sum())
    return df['Irrigation Scheduling'].sum()



# table = tabulate(df, headers=df.columns, tablefmt='outline')
# print(table)
print(optimizer(temp))
