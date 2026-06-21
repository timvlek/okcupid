def fit_pipelines(pipelines, x_train, y_train, class_weight='balanced', class_weights, sample_weight):
         
    # Populate the dictionary with fitted pipelines.
    from IPython.utils import io
    with io.capture_output():
        for name, pipeline in pipelines.items():
            if name = 'KNN':
                pipeline.fit(X=x_train, y=y_train)
            elif name == 'LightGBM':
                pipeline.fit(X=x_train, y=y_train, classifier__class_weight='balanced')
            elif name == 'CatBoost':
                pipeline.fit(X=x_train, y=y_train, classifier__class_weights=class_weights)
            else:
                pipeline.fit(X=x_train, y=y_train, classifier__sample_weight=sample_weight)
    
    return