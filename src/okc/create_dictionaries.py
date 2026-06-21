def create_dictionaries(df):
    
    global column_units 
    global multi_index
    global column_features
    global columns_features_units
    global features_units
    global multi_index
    
    # Define a dictionary of columns and data units
    column_units = {column: unit if unit else '' for column, unit in zip(df.columns, units)}

    # Define a dictionary of columns and data labels
    column_features = {column: feature for column, feature in zip(df.columns, features)}

    # Define a dictionary of columns and data labels and units
    columns_features_units = {
        column: ' '.join([feature, unit]) if unit else feature for column, feature, unit in zip(df.columns, features, units)}

    # Define a tuple of features and units
    features_units = [(feature, unit) if unit else (feature, '') for feature, unit in zip(features, units)]

    # Define a multi-index
    multi_index = pd.MultiIndex.from_tuples(features_units, names=["Feature", "Unit"])

    # Set dataframe columns to the multi-index
    # df.columns = multi_index

    # Replace data values.
    return