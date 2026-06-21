def calculate_train_residuals(X_train, y_train, model):
    
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    
    train_residuals = pd.DataFrame()
    train_residuals[y_train.name] = y_train
#     residuals['Transformed {}'.format(y_train.name)] = ttr.transformer.func(y_train)
    train_residuals['Observations'] = y_train
    train_residuals['Standardized observations'] = StandardScaler().fit_transform(pd.DataFrame(y_train))
    train_residuals['Predictions'] = model.predict(X_train)
    train_residuals['Residuals'] = train_residuals['Observations'] - train_residuals['Predictions']
    train_residuals['Standardized residuals'] = StandardScaler().fit_transform(train_residuals[['Residuals']])
    return train_residuals


def calculate_test_residuals(X_train, X_test, y_train, y_test, model):
    
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    
    test_residuals = pd.DataFrame()
    test_residuals[y_test.name] = y_test
#     residuals['Transformed {}'.format(y_test.name)] = ttr.transformer.func(y_test)
    test_residuals['Observations'] = y_test
    test_residuals['Standardized observations'] = StandardScaler().fit(pd.DataFrame(y_train)).transform(pd.DataFrame(y_test))
    test_residuals['Predictions'] = model.predict(X_test)
    test_residuals['Residuals'] = test_residuals['Observations'] - test_residuals['Predictions']
    test_residuals['Standardized residuals'] = StandardScaler().fit_transform(test_residuals[['Residuals']])
    return test_residuals

def calculate_residuals(X_train, X_test, y_train, y_test, model):
    '''
    Calculate residuals of a regression model.

    Parameters
    ----------
    X_train : pandas.core.frame.DataFrame
        Training split of the independent features
    X_test : pandas.core.frame.DataFrame
        Test split of the independent features
    y_train : pandas.core.series.Series
        Training split of the dependent feature
    y_test : pandas.core.series.Series
        Test split of the dependent feature
    
    Returns
    -------
    residuals : pandas.core.frame.DataFrame
        (new) DataFrame with residuals.
    '''
       
    import pandas as pd
    from sklearn.preprocessing import StandardScaler

    train_residuals = calculate_train_residuals(X_train, y_train, model)
    test_residuals = calculate_test_residuals(X_train, X_test, y_train, y_test, model)
    train_residuals['Split'] = ['Train'] * len(train_residuals)
    test_residuals['Split'] = ['Test'] * len(test_residuals)
    residuals = pd.concat([train_residuals, test_residuals], axis=0)
    residuals.sort_index(axis=0, inplace=True)
    return residuals

def add_split_column(df, split, inplace=False):
    '''
    Add a column named 'Split' to a dataframe and fill the values.  

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        DataFrame to add the 'Split' column to.
    split : str
        The values of the 'Split' column. 
    
    Returns
    -------
    df : pandas.core.frame.DataFrame
        (new) DataFrame with a 'Split' column and values.
    '''
            
    if inplace == False:
        new_df = df.copy()
        new_df['Split'] = len(df) * [split]
        return new_df
    elif inplace == True:
        df['Split'] = len(df) * [split]
        return df
    else:
        print('Error')

def calculate_model_scores(X, y, X_train, X_test, y_train, y_test, model, cv):
    
    from sklearn.model_selection import cross_val_score
    from sklearn.metrics import make_scorer
    from sklearn.metrics import mean_absolute_error
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import r2_score
    import pandas as pd
    
    mae = make_scorer(mean_absolute_error)
    mse = make_scorer(mean_squared_error)
    
    model_scores = pd.DataFrame({
        'Estimator': [str(model.named_steps.classifier).split('(')[0]],
        'Train R²': [r2_score(y_train, model.predict(X_train))],
        'Test R²': [r2_score(y_test, model.predict(X_test))],
        'CV R²': [cross_val_score(model, X, y, scoring='r2', cv=cv).mean()],
        'Train MAE': [mae(y_train, model.predict(X_train))],
        'Test MAE': [mae(y_test, model.predict(X_test))],
        'CV MAE': [cross_val_score(model, X, y, scoring=mae, cv=cv).mean()],
        'Train RMSE': [mse(y_train, model.predict(X_train))**.5],
        'Test RMSE': [mse(y_test, model.predict(X_test))**.5],
        'CV RMSE': [cross_val_score(model, X, y, scoring=mse, cv=cv).mean()**.5],
    })
    
    return model_scores

def print_model_scores(scores):
                                
    output = f'''
        Estimator: {scores.values[0,0]}

        Train R²: {scores.values[0,1]:,.2f}
        Test R²: {scores.values[0,2]:,.2f}
        CV R²: {scores.values[0,3]:,.2f}
        
        Train MAE: {scores.values[0,4]:,.2f}
        Test MAE: {scores.values[0,5]:,.2f}
        CV MAE: {scores.values[0,6]:,.2f}
    
        Train RMSE: {scores.values[0,7]:,.2f}
        Test RMSE: {scores.values[0,8]:,.2f}
        CV RMSE: {scores.values[0,9]:,.2f}
    '''
    
    print(output)

def save_model_scores(all_model_scores, scores):
    
    all_model_scores.loc[scores.values[0,0], 'Estimator'] = scores.values[0,0]
    all_model_scores.loc[scores.values[0,0], 'Train R²'] = scores.values[0,1]
    all_model_scores.loc[scores.values[0,0], 'Test R²'] = scores.values[0,2]
    all_model_scores.loc[scores.values[0,0], 'CV R²'] = scores.values[0,3]
    all_model_scores.loc[scores.values[0,0], 'Train MAE'] = scores.values[0,4]
    all_model_scores.loc[scores.values[0,0], 'Test MAE'] = scores.values[0,5]
    all_model_scores.loc[scores.values[0,0], 'CV MAE'] = scores.values[0,6]
    all_model_scores.loc[scores.values[0,0], 'Train R'] = scores.values[0,7]
    all_model_scores.loc[scores.values[0,0], 'Test RMSE'] = scores.values[0,8]
    all_model_scores.loc[scores.values[0,0], 'CV RMSE'] = scores.values[0,9]
    
    return

def print_all_model_scores(scores):
    
    import seaborn as sns

    m = sns.light_palette("green", as_cmap=True)
    styler = scores.style.format(
        precision=2
    ).text_gradient(
        cmap=m, 
        subset=['Train R²', 'Test R²', 'CV R²',], 
        low=sorted(scores['Train R²'])[3],
        high=max(scores['Train R²'])
    ).text_gradient(
        cmap=m.reversed(),
        subset=['Train MAE', 'Test MAE', 'CV MAE', 'Train RMSE', 'Test RMSE', 'CV RMSE'],
    ).hide(axis='index')
    
    return styler


def plot_all_model_scores(scores):
    sns.barplot()
    
def calculate_cv_scores(model, X_train, X_test, y_train, y_test, cv):
    
    from sklearn.model_selection import cross_val_score
    from sklearn.metrics import make_scorer
    from sklearn.metrics import mean_absolute_error
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import r2_score
    import pandas as pd
    
    r2 = make_scorer(r2_score)
    mae = make_scorer(mean_absolute_error)
    mse = make_scorer(mean_squared_error)
        
    train_scores = pd.DataFrame({
        'Estimator': [str(model.named_steps.classifier).split('(')[0]] * cv.n_splits,
        'Split': ['Train'] * cv.n_splits,
        'R²': cross_val_score(model, X_train, y_train, scoring=r2, cv=cv),
        'MAE': cross_val_score(model, X_train, y_train, scoring=mae, cv=cv),
        'RMSE': [score**.5 for score in cross_val_score(model, X_train, y_train, scoring=mse, cv=cv)],

    })
    
    test_scores = pd.DataFrame({
        'Estimator': [str(model.named_steps.classifier).split('(')[0]] * cv.n_splits,
        'Split': ['Test'] * cv.n_splits,
        'R²': cross_val_score(model, X_test, y_test, scoring=r2, cv=cv),
        'MAE': cross_val_score(model, X_test, y_test, scoring=mae, cv=cv),
        'RMSE': [score**.5 for score in cross_val_score(model, X_test, y_test, scoring=mse, cv=cv)]
    })
    
    scores = pd.concat([train_scores, test_scores])
    return scores


def transform_df(pipe, X_train, y_train):
    
    import pandas as pd
    
    features = get_features_in(pipe)
    data = pipe[:-1].fit_transform(X_train)
    transformed_df = pd.DataFrame(data=data, columns=features)
    transformed_df[y_train.name] = y_train
    
    return transformed_df

def to_superscript(num):
    '''Transform an integer to it's superscript'''
    
    transl = str.maketrans(dict(zip('1234567890', '¹²³⁴⁵⁶⁷⁸⁹⁰')))
    return num.translate(transl)

# def get_coefficients(pipe):
    
#     import pandas as pd
    
#     coef_ = pipe.named_steps['classifier'].coef_
#     ohe_names = pipe.named_steps['encoder'].get_feature_names_out()

#     ohe_dict = {}
#     ohe_dict['1'] = '1'
#     for i in range(len(ohe_names)):
#         ohe_name = ohe_names[i].split("_", 3)[-1]
#         ohe_dict['x{}'.format(i)] = ohe_name
#     # ohe_dict

#     poly_names = pipe.named_steps['engineering'].get_feature_names_out()
#     # poly_names

#     import re
#     poly_names = [re.sub(' ', ' * ', feature) for feature in poly_names]
#     poly_names = [re.sub('\^\s*(\d+)', lambda m: to_superscript(m[1]), feature) for feature in poly_names]
#     for ohe, name in ohe_dict.items():
#         for i in range(len(poly_names)):

#             feature = poly_names[i]
#             feature = feature.replace(ohe, name)
#             poly_names[i] = feature


#     coefficients = pd.DataFrame(columns=['Parameter', 'Coefficient'])
#     for name, coefficient in zip(poly_names, coef_):
#         if coefficient != 0:
#             coefficients = pd.concat(
#                 [
#                     coefficients, 
#                     pd.DataFrame([[name, coefficient]], columns=['Parameter', 'Coefficient'])
#                 ],
#                 ignore_index = True, 
#                 axis = 0
#             )

#     coefficients.sort_values(by='Coefficient', key=abs, ascending=False, inplace=True)
#     coefficients.reset_index(drop=True, inplace=True)
   
#     return coefficients

def get_features_in(pipe):
    
    import pandas as pd
    
    ohe_names = pipe.named_steps['encoder'].get_feature_names_out()

    ohe_dict = {}
    ohe_dict['1'] = '1'
    for i in range(len(ohe_names)):
        ohe_name = ohe_names[i].split("_", 3)[-1]
        ohe_dict['x{}'.format(i)] = ohe_name

    import re
    poly_names = pipe.named_steps['engineering'].get_feature_names_out()   
    poly_names = [re.sub(' ', ' * ', feature) for feature in poly_names]
    poly_names = [re.sub('\^\s*(\d+)', lambda m: to_superscript(m[1]), feature) for feature in poly_names]
    for ohe, name in ohe_dict.items():
        for i in range(len(poly_names)):
            feature = poly_names[i]
            feature = feature.replace(ohe, name)
            poly_names[i] = feature
    
    return poly_names

def get_coefficients(pipe):
    
    import pandas as pd
    
    coefficients_df = pd.DataFrame(columns=['Parameter', 'Coefficient'])
    features_in = get_features_in(pipe)
    coefficients = pipe.named_steps['classifier'].coef_
    for name, coefficient in zip(features_in, coefficients):
        if coefficient != 0:
            coefficients_df = pd.concat(
                [
                    coefficients_df, 
                    pd.DataFrame([[name, coefficient]], columns=['Parameter', 'Coefficient'])
                ],
                ignore_index = True, 
                axis = 0
            )

    coefficients_df.sort_values(by='Coefficient', key=abs, ascending=False, inplace=True)
    coefficients_df.reset_index(drop=True, inplace=True)
   
    return coefficients_df