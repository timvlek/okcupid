def insignificant_features(X_train, y_train):
    '''
    Determine insignificant features of a linear regression model.
    
    Fits an ordinary least squares multiple linear regression model.
    Subsequently eliminates the most insignificant feature (largest p-value).
    Repeats this proces until all insignificant features are removed.
    
    Parameters
    ----------
    X_train : pandas.core.frame.DataFrame
        DataFrame of the indepedent features.
    y_train : pandas.core.series.Series
        Series of the dependent feature.
           
    Returns
    -------
    independent_features : list
        The independent features used in the final fitted linear regression model.
    '''

    x = sm.add_constant(X_train)
    OLS = sm.OLS(y_train, X_train)
    OLSResults = OLS.fit()
    
    while any(OLSResults.pvalues > .05):
        most_insignificant_feature = OLSResults.pvalues.idxmax()
        x = x.drop(labels=most_insignificant_feature, axis=1)
        OLS = sm.OLS(y_train, x)
        OLSResults = OLS.fit()
        
    independent_features = OLS.exog_names
    independent_features.remove('const')
    independent_features.sort()
    return independent_features

def forwards_feature_elimination(X_train, y_train, model):
    '''
    Determine insignificant features of a linear model.

    Parameters
    ----------
    X_train : pandas.core.frame.DataFrame
        DataFrame of the indepedent features.
    y_train : pandas.core.series.Series
        Series of the dependent feature.
    model : sklearn.linear_model
        An instance of a model from the sklearn.linear_model library.
           
    Returns
    -------
    independent_features : list
        The independent features used in the fitted linear model.
    model : sklearn.linear_model
        An instance of a fitted model from the sklearn.linear_model library.
    '''
    
    from itertools import combinations
    features = X_train.columns.tolist()
    independent_features = []
    old_set_rsquared_adj = 0
    new_set_rsquared_adj = .001
    N = len(X_train)
    k = len(features)    
    remaining_features = features    
    while new_set_rsquared_adj > old_set_rsquared_adj:

        for k in range(1, len(features) + 1):
            features = [feature for feature in features if feature not in independent_features]
            feature_lists = [independent_features + [feature] for feature in features]
            old_set_rsquared_adj = new_set_rsquared_adj
            # Create and loop over all feature combinations:
            for feature_list in feature_lists:
                # Perform linear regression.
                with io.capture_output() as captured:
                    model.fit(X_train[feature_list], y_train)

                # Calculate rsquared and adjust it to account for the use of multiple predictors.
                rsquared = model.score(X_train[feature_list], y_train)
                rsquared_adj = 1 - (1-rsquared**2) * (N-1) / (N-k-1)
                if rsquared_adj > new_set_rsquared_adj:
                    independent_features = feature_list
                    new_set_rsquared_adj = rsquared_adj              
    independent_features.sort()
    model.fit(X_train[independent_features], y_train)
    return independent_features, model