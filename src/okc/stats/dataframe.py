import pandas as pd

def dataframe(df: pd.DataFrame) -> pd.DataFrame:
    stats_df = pd.DataFrame({
        'No. rows': [len(df)], 
        'No. columns': [len(df.columns)], 
        'No. duplicated rows': [df.duplicated().sum()],
    })
    
    return stats_df