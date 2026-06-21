# def rename_columns(df, columns, names, copy=True, inplace=False)

#     '''
#     Rename DataFrame columns to be more self explanatory.
#     The lists of columns and names provided, should be of equal length.
    
#     Parameters
#     ----------
#     df : pandas.core.frame.DataFrame
#         DataFrame with data to be analysed.
#     columns: list
#         List of column names, which values should be renamed.
#     names: list
#         List of new names for the columns.
#     copy: bool, default True
#         Also copy underlying data.
#     inplace: bool, default False
#         Whether to return a new DataFrame. If True then value of copy is ignored.
    
#     Returns
#     -------
#     DataFrame or None
#          DataFrame with all provided columns scaled or None if inplace=True.
#     '''
    
#     import pandas as pd
    
#     if len(columns) != len(names):
#         return 'The lists of columns and names provided, should be of equal length.'
    
#     if inplace==False:
#         if copy==True:
#             renamed_df = df.copy()
#             for column, factor in zip(columns, factors):
#                 renamed_df[column] = renamed_df[column]
#             return scaled_df
#         elif copy==False:
#             for column, factor in zip(columns, factors):
#                 df[column]= df[column]/factor
#             return df
#     if inplace==True:
#         for column, factor in zip(columns, factors):
#             df[column]= df[column]/factor
#         return
    
def convert_column_dtypes(df, convert_type=None, to_type=None, inplace=False):

    if inplace == False:
        new_df = df.copy()
        for column in new_df.select_dtypes(include=convert_type).columns.tolist():
            new_df[column] = new_df[column].astype(to_type)
        return new_df
    
    elif inplace == True:
        for column in df.select_dtypes(include=convert_type).columns.tolist():
            df[column] = df[column].astype(to_type)
        return

def rename_categories(df, categories, inplace=False):
    
    if inplace == False:
        new_df = df.copy()
        for column, categories in categories.items():
            for value, new_value in categories.items():
                new_df[column] = df[column].replace(value, new_value, inplace=False)
        return new_df

    if inplace == True:
        for column, categories in categories.items():
            for value, new_value in categories.items():
                df[column].replace(value, new_value, inplace=True)
        return
                
def capitalize_df_values(df, inplace=False):
    
    if inplace == False:
        new_df = df.copy()
        for column in new_df.select_dtypes(include='category').columns.tolist():
            new_df[column] = new_df[column].map(lambda x: x.title())
        return new_df
    
    if inplace == True:
        for column in df.select_dtypes(include='category').columns.tolist():
            df[column] = df[column].map(lambda x: x.title())
        return
    
def rename_column_categories(df, inplace=False):
    
    if inplace == False:
#         new_df = df.copy()
#         for column in new_df.select_dtypes(include='category').columns.tolist():
#             new = input('Do you wish to input new category values for: {}/nType either Y or N'.format(df[column].cat.categories))
#             if new.capitalize() == 'N':
#                 continue
#             elif new.capitalize() == 'Y':
#                 for category in new_df[column].cat.categories:
#                     new_category = input('Please input new name for category: {}'.format(category))
#                     new_df[column].replace(category, new_category)
#         return new_df
        pass

    elif inplace == True:
        for column in df.select_dtypes(include='category').columns.tolist():
            print('2')
            new = input('Do you wish to input new category values for: {}/nType either Y or N'.format(df[column].cat.categories))
            if new.capitalize() == 'N':
                continue
            elif new.capitalize() == 'Y':
                for category in df[column].cat.categories:
                    new_category = input('Please input new name for category: {}'.format(category))
                    df[column].replace(category, new_category)
        return