def create_visualization_df(df, labels):
    '''
    Rename all columns of a DataFrame to be more meaningfull.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with columns to rename.
    labels : list
        The new names of the DataFrame columns.
        
    Returns
    -------
    visualization_df : pandas.core.frame.DataFrame
        DataFrame with columns renamed.
    '''
    
    import pandas as pd
    
    # Create dataframe for visualizations
    visualization_df = df.copy()

    # Capitalize data values
    categorical_features = list(visualization_df.select_dtypes(include=['object', 'category']).columns)
    for category in categorical_features:
        visualization_df[category] = visualization_df[category].str.capitalize()

    # Create 'No_children' as an ordinal feature, because of the limited number of options.
    visualization_df.children = pd.Categorical(
        visualization_df.children, 
        categories = sorted(visualization_df.children.unique()), 
        ordered =  True
    )

    # Convert object to categorical features.
    for feature in categorical_features:
        visualization_df[feature] = visualization_df[feature].astype('category')
    
    # Rename dataframe columns
    visualization_df.columns = labels
    
    return visualization_df

def to_superscript(num):
    '''Transform an integer to it's superscript'''
    
    transl = str.maketrans(dict(zip('1234567890', '¹²³⁴⁵⁶⁷⁸⁹⁰')))
    return num.translate(transl)

def add_polynomials(df, degree=2, interaction_only=False, include_bias=True, order='C', columns=None):
    '''
    Add polynomials to a dataframe
    
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with polynomials to add.
    degree : int, default=2
        The maximal degree of the polynomial features.
        Note that min_degree=0 and min_degree=1 are equivalent as outputting the degree zero term is determined by include_bias.
    interaction_only : bool, default=False
        If True, only interaction features are produced: 
        features that are products of at most degree distinct input features, 
        i.e. terms with power of 2 or higher of the same input feature are excluded:
                included: x[0], x[1], x[0] * x[1], etc.
                excluded: x[0] ** 2, x[0] ** 2 * x[1], etc.
    include_bias : bool, default=True
        If True (default), then include a bias column, 
        the feature in which all polynomial powers are zero 
        (i.e. a column of ones - acts as an intercept term in a linear model).
    order : {‘C’, ‘F’}, default=’C’
        Order of output array in the dense case. 
        'F' order is faster to compute, but may slow down subsequent estimators.
    columns : list, default=None
        Columns to log transform.
        If no columns are provided, polynomials are created from all numerical columns.
           
    Returns
    -------
    polynomial_df : pandas.core.frame.DataFrame
        DataFrame with columns log transformed.
    '''
    
    # Add polynomial features for use in regression
    if columns == None:
        numerical_features = list(df.select_dtypes(exclude=['object', 'category']).columns)
        categorical_features = list(df.select_dtypes(include=['object', 'category']).columns)
    else:
        numerical_features = columns
        categorical_features = [column for column in df.columns if column not in numerical_features]
        
    poly = PolynomialFeatures(degree)
    poly.fit_transform(df[numerical_features])
    polynomial_features = poly.get_feature_names(numerical_features)
#     polynomial_features = poly.get_feature_names_out(numerical_features)
    polynomial_features = [re.sub('\^\s*(\d+)', lambda m: to_superscript(m[1]), feature) for feature in polynomial_features]
    polynomial_features = [feature.replace(' ', ' * ') for feature in polynomial_features]
    polynomial_features = [feature.replace('No. * children', 'No. children') for feature in polynomial_features]
    polynomial_df = pd.DataFrame(
        poly.fit_transform(df[numerical_features]), 
        columns = polynomial_features,
        index = df.index
    )
    polynomial_df = df[categorical_features].join(polynomial_df)
    polynomial_df = polynomial_df.drop(labels='1', axis=1)
    polynomial_df.sort_index(axis=1, inplace=True)
    
    return polynomial_df

def log_transform(df, columns=None):
    '''
    Log transform columns of a dataframe.
    
    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with columns to log transform.
    columns : list, default=None
        Columns to log transform.
        If no columns are provided, all numerical columns will log transformed.
           
    Returns
    -------
    df : pandas.core.frame.DataFrame
        DataFrame with columns log transformed.
    '''

    import numpy as np
    if columns == None:
        numerical_features = list(df.select_dtypes(exclude=['object', 'category']).columns)
        categorical_features = list(df.select_dtypes(include=['object', 'category']).columns)
    else:
        numerical_features = columns
        categorical_features = [column for column in df.columns if column not in numerical_features]
        
    transformed_df = pd.DataFrame()
    
    for feature in numerical_features: 
        transformed_df[feature] = np.log(df[feature] + .001)
    
    transformed_df = pd.concat([transformed_df, df[categorical_features]], axis=1)
    polynomial_df.sort_index(axis=1, inplace=True)
    
    return transformed_df

def standardize_numericals(df, columns=None):
    '''
    Standardize columns of a dataframe.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with columns to encode.
    columns : list, default=None
        Columns to standardize.
        If no columns are provided, all numerical columns will be standardized.
           
    Returns
    -------
    df : pandas.core.frame.DataFrame
        DataFrame with columns standardized.
    '''
    
    # Standardize numerical features to 
    # reduce multicollinearity and improve interpretability of regression
    from sklearn import StandardScaler
    if columns == None:
        numerical_features = list(df.select_dtypes(exclude=['object', 'category']).columns)
        categorical_features = list(df.select_dtypes(include=['object', 'category']).columns)
    else:
        numerical_features = columns
        categorical_features = [column for column in df.columns if column not in numerical_features]
        
    transformed_df = pd.DataFrame(index = df.index)
    transformed_df[numerical_features] = StandardScaler().fit_transform(df[numerical_features])
    transformed_df = pd.concat([transformed_df, df[categorical_features]], axis=1)
    transformed_df.sort_index(axis=1, inplace=True)
    return transformed_df

def nominal_encode(df, columns=None):
    '''
    Nominal encode columns of a dataframe.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame with columns to encode.
    columns : list, default=None
        Columns to encode.
        If no columns ar provided, all categorical columns will be encoded.
           
    Returns
    -------
    df : pandas.core.frame.DataFrame
        DataFrame with columns encoded.
    '''
    
    # label encode binary features for use in regression
    import pandas as pd
    if columns == None:
        categorical_features = list(df.select_dtypes(include=['object', 'category']).columns)
    else:
        categorical_features = columns
    
    print(categorical_features)
    nominal_features = [feature for feature in categorical_features if df[feature].cat.ordered == False]
    ordinal_features = [feature for feature in nominal_features if df[feature].nunique() > 2]
    binary_features = [feature for feature in nominal_features if df[feature].nunique() <= 2]
    transformed_df = df.drop(columns=nominal_features, axis=1)

#     transformed_df = pd.DataFrame()
    for feature in binary_features:
        transformed_df[feature] = pd.get_dummies(df[feature], drop_first=True)   

    # df.smoking = 0 - df.smoking

    # One Hot Encode nominal features for use in regression
    
    for feature in ordinal_features:
        ordinal_df = pd.get_dummies(df[feature], prefix='{}'.format(feature), prefix_sep='_', drop_first=True)
        transformed_df = pd.concat([transformed_df, ordinal_df], axis=1)
    transformed_df.sort_index(axis=1, inplace=True)
    return transformed_df

def transform_features(X):
    '''
    Transform features of a dataframe.
    
    Add polynomials.
    Log transform the numerical features.
    Encode the nominal features.
    Standardize all features.
    
    Parameters
    ----------
    X : pandas.core.frame.DataFrame
        DataFrame of the indepedent features.
           
    Returns
    -------
    independent_features : list
        The independent features used in the final fitted linear regression model.
    '''   
    transformed_df = add_polynomials(df, degree=3)
    transformed_df = log_transform(transformed_df)
    transformed_df = nominal_encode(transformed_df)
    transformed_df = standardize_numericals(transformed_df)
    return transformed_df
