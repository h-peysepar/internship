import pandas as pd
from math import prod

def read_input(cellName):
    df = pd.read_excel('data.xlsx', sheet_name='Input', skiprows=1, nrows=3, usecols="A:B")
    df.columns = ['key', 'value']
    key_row = df[df['key'] == cellName]
    
    if not key_row.empty:
        value = key_row.iloc[0]['value']
        return value
    else:
        return None


def get_expected_productivity():
    return read_input('Expected Crop Yeild')


def get_max_productivity():
    df = pd.read_excel('data.xlsx', sheet_name='Crop History', skiprows=1, nrows=9, usecols="B:B")
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
            df.loc[i, cycle_key] = df.loc[i : i + jump - 1, 'Irrigation Scheduling'].sum()



