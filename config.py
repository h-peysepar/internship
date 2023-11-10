config = {
    "SOIL_WATER_SOLIITY": 5,
    "IRRIGATION_FREQUENCY": 40,
    "EXPECTED_CROP_YEILD": 5000,
    "FIELD_CAPACITY": 157.5,
    "AGE": 10,
    "MAX_CROP_EFFICIENCY": 8333,

}


def read_config(key):
    global config
    return config[key] or None
    
