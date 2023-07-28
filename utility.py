import pandas as pd
from math import prod

inputSheet = pd.read_excel('data.xlsx', sheet_name='Input', skiprows=1, nrows=5, usecols="A:B")
cropHistory = pd.read_excel('data.xlsx', sheet_name='Crop History', skiprows=1, nrows=9, usecols="B:B")

def read_input(cellName):
    global inputSheet
    df = inputSheet
    df.columns = ['key', 'value']
    key_row = df[df['key'] == cellName]
    
    if not key_row.empty:
        value = key_row.iloc[0]['value']
        return value
    else:
        return None


def get_expected_productivity():
    expected = read_input('Expected Crop Yeild')
    sws = read_input('Soil Water Solidity')
    age = read_input('Age')
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


def get_max_productivity():
    global cropHistory
    df = cropHistory
    df.columns = ['Efficiency']
    maxCropEfficiency = df['Efficiency'].max()
    return maxCropEfficiency


def create_dataframe():
    df = pd.read_excel('data.xlsx', sheet_name='Irrigation', skiprows=1, nrows=23, usecols="A:H")
    df.columns = ['Month', 'Decade', 'Progress Stage', 'Kc', 'ETo', 'ETc', 'Effective Precipitation', 'Irrigation']
    return df


def calculate_columns(df):
    df['Raes Method1'] = df['Progress Stage'] * (df['Irrigation Scheduling'] / df['Irrigation'])
    df['Raes Method2'] = 1 - df['Raes Method1']
    df['Raes Method3'] = pow(df['Raes Method2'], 10/220)
    df['Raes Method4'] = 1 - df['Raes Method3']
    cycle = read_input('Irrigation Frequency')
    cycle_key = f'Irrigation Scheduling F={cycle}'
    df[cycle_key] = None
    jump = cycle / 10
    for i in range(0, len(df)):
        if (i % jump) == 0:
            sum = df.loc[i : i + jump - 1, 'Irrigation Scheduling'].sum()
            capacity = read_input('Field Capacity')
            df.loc[i, cycle_key] = sum if capacity > sum else capacity 



