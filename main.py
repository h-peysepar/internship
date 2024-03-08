import pandas as pd
from tabulate import tabulate
from math import prod
from scipy.optimize import minimize

def get_expected_productivity(field_info):
    expected = field_info['EXPECTED_CROP_YEILD']
    sws = field_info['SOIL_WATER_SOLINITY']
    age = field_info['AGE']
    # apply salinity condition
    if sws and sws > 7:
        expected = 100 - 3.6 * (expected - 7)
    # apply age condition
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
    # Raes calculations
    df['Raes Method1'] = df['Progress Stage'] * \
        (df['Irrigation Scheduling'] / df['Irrigation'])
    df['Raes Method2'] = 1 - df['Raes Method1']
    df['Raes Method3'] = pow(df['Raes Method2'], 10/220)
    df['Raes Method4'] = 1 - df['Raes Method3']



def optimizer(field_info, plant_info):
    df = create_dataframe(plant_info)
    df['Irrigation Scheduling'] = df['Irrigation']
    calculate_columns(df)


    # this function calculate errors.
    def calculate_objective(df):
        product = df['Raes Method3'].product()
        max = field_info["MAX_CROP_EFFICIENCY"]
        expected = get_expected_productivity(field_info)
        objective = expected - ((1 - product) * max)
        return objective

    # minimize errors
    def objective_function(x, df):
        df['Irrigation Scheduling'] = x
        calculate_columns(df)
        objective = calculate_objective(df)
        return abs(objective)

    # constraint (less irrigation water)
    def constraint(x, x_values, y_values):
        return y_values - x_values

    ## optimize values with `minimize` function
    result = minimize(
        objective_function,
        df['Irrigation Scheduling'].values,
        args=(df,),
        constraints={
            'type': 'ineq',
            'fun': constraint,
            'args': (
                df['Irrigation'].values,
                df['Irrigation Scheduling'].values
            ),
        },
        bounds=[(0, None)])

    optimized_y_values = result.x

    ## apply optimized values
    df['Irrigation Scheduling'] = optimized_y_values
    calculate_columns(df)

    optimized_objective = calculate_objective(df)
    output = df['Irrigation Scheduling'].sum()* field_info['AREA']
    print(f"Total Irrigation Water for {field_info['NAME']}: ",output)
    return  output



## Enter the data of as many fields as you want
fields = [
    {
        'plant_info': {
            'Progress Stage': [.5], # ضریب مرحله رشد گیاه
            'Kc': [.38],
            'ETo': [40.74],
            'ETc': [12.19],
            'Effective Precipitation': [2.36], #میلیمتر بر دهه
            'Irrigation': [9.83], # میلیمتر بر دهه
        },
        'field_info': {
            "NAME": "MR. Asghari field",
            "SOIL_WATER_SOLINITY": 5,
            "IRRIGATION_FREQUENCY": 40, #day
            "EXPECTED_CROP_YEILD": 5000, #kg
            "FIELD_CAPACITY": 157.5,
            "AGE": 10, # year
            "MAX_CROP_EFFICIENCY": 8333, #kg
            "AREA": 1 # hectares 
        }
    },
    {
        'plant_info': {
            'Progress Stage': [.5], # ضریب مرحله رشد گیاه
            'Kc': [.38],
            'ETo': [40.74],
            'ETc': [12.19],
            'Effective Precipitation': [2.36], #میلیمتر بر دهه
            'Irrigation': [9.83], # میلیمتر بر دهه
        },
        'field_info': {
            "NAME": "MR. Akbari field",
            "SOIL_WATER_SOLINITY": 5,
            "IRRIGATION_FREQUENCY": 40, #day
            "EXPECTED_CROP_YEILD": 5000, #kg
            "FIELD_CAPACITY": 157.5,
            "AGE": 10, # year
            "MAX_CROP_EFFICIENCY": 8333, #kg
            "AREA": 1# hectares
        }
    },
    ## other fields data..
]

for index, field in enumerate(fields):
    optimizer(**field)

