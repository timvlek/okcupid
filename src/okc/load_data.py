# Load csv data and import them into a pandas DataFrame
def load_data():
    import pandas as pd
    data = pd.read_csv('insurance.csv')
    df = pd.DataFrame(data)
    return df