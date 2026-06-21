import calendar

def extract_datetime_features(df, column, inplace=True):
    """Extracts common features from a datetime column.

    Args:
        df (pandas.DataFrame): The DataFrame containing the datetime column.
        column (str): The name of the datetime column.

    Returns:
        pandas.DataFrame: A new DataFrame with the extracted features.
    """

    features = {
        column + ': year': 'year',
        column + ': month': 'month',
        column + ': day': 'day',
        column + ': hour': 'hour',
        column + ': day of week': 'dayofweek',
        # column + '_dayofyear': 'dayofyear',
        # column + '_is_weekday': 'is_weekday',
        # column + '_is_weekend': 'is_weekend',
        column + ': quarter': 'quarter'
    }

    if inplace:
        for feature, dt_property in features.items():
            df[feature] = df[column].dt.__getattribute__(dt_property)
            if feature == 'is_weekday':
                new_df[feature] = new_df[feature].astype(bool)
            elif feature == 'is_weekend':
                new_df[feature] = ~new_df[feature]
        return
    
    else:
        new_df = df.copy()
        for feature, dt_property in features.items():
            new_df[feature] = new_df[column].dt.__getattribute__(dt_property)
        return new_df