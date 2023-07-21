import pandas as pd
from math import prod


def get_efficiency(df, max):
    array = df['Raes Method3'].values
    # print(array)
    converted = []
    for val in array:
        if val > 0:
            converted.append(val)
    result = prod(converted)

    print(result)
    return (1 - result) * max


def get_expected_productivity():
    return 5000


def get_max_productivity():

    df = pd.read_excel('data.xlsx', skiprows=16, nrows=17, usecols="L:L")

    df.columns = ['Efficiency']

    df = df[df['Efficiency'] > 0]

    array = df['Efficiency'].values

    last8YearEfficiency = df['Efficiency'].mean()

    # print('Crop Efficiency In Last 8 Years:', last8YearEfficiency)

    maxCropEfficiency = df['Efficiency'].max()

    return maxCropEfficiency


def create_dataframe():

    df = pd.read_excel('data.xlsx', skiprows=102, nrows=23, usecols="A:H")

    # print(df)

    df.columns = ['Month', 'decade', 'progress level',
                  'Kc', 'ETo', 'ETc', 'Pe', 'IR']
    return df


def calculate_columns(df):

    df['Raes Method1'] = .5 * (df['Irrig. Scheduling F=10'] / df['IR'])

    df['Raes Method2'] = 1 - df['Raes Method1']

    df['Raes Method3'] = pow(df['Raes Method2'], 10/220)

    df['Raes Method4'] = 1 - df['Raes Method3']

    df['Irrig. Scheduling F=30'] = None

    for i in range(0, len(df), 3):

        df.loc[i, 'Irrig. Scheduling F=30'] = ''

        df.loc[i+2, 'Irrig. Scheduling F=30'] = ''

        df.loc[i+1, 'Irrig. Scheduling F=30'] = df.loc[i:i +

                                                       2, 'Irrig. Scheduling F=10'].sum()

    # print(df)

    # real_productivity =

    # return {'real_productivity': }
