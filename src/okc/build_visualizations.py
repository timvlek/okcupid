from IPython.utils import io
import seaborn as sns
import matplotlib.pyplot as plt    

# Define the groups of features with identical data types.

def plot_histograms(visualization_df):
    '''
    Plot histograms of all numerical features.

    Parameters
    ----------
    visualization_df : pandas.core.frame.DataFrame
        DataFrame to visualize.
    '''
    
    from math import ceil
    from itertools import combinations
    
    age_bins = [0 + i for i in range(ceil(visualization_df.Age.max())+2)]
    numerical_features = list(visualization_df.select_dtypes(exclude=['object', 'category']).columns)
    categorical_features = list(visualization_df.select_dtypes(include=['object', 'category']).columns)
    
    for numerical_feature in numerical_features: 
        for categorical_feature in categorical_features:
            with io.capture_output() as captured:
                sns.histplot(
                    data = visualization_df,
                    x = numerical_feature,
                    hue = categorical_feature, 
                    stat="count", 
                    multiple="stack"
                )
                plt.xlim(xmin=0)
                plt.ylim(ymin=0)
                plt.title('Distribution of {}'.format(numerical_feature.lower()))
                plt.ylabel('No. customers')
                plt.tight_layout()
            plt.show()
            plt.close()
            
        
def plot_histograms(visualization_df):
    '''
    Plot histograms of all numerical features.
    
    Parameters
    ----------
    visualization_df : pandas.core.frame.DataFrame
        DataFrame to visualize.
    '''
    
    from math import ceil
    from itertools import combinations
    
    age_bins = [0 + i for i in range(ceil(visualization_df.Age.max())+2)]
    numerical_features = list(visualization_df.select_dtypes(exclude=['object', 'category']).columns)
    categorical_features = list(visualization_df.select_dtypes(include=['object', 'category']).columns)
    
    for numerical_feature in numerical_features: 
        for categorical_feature in categorical_features:
            with io.capture_output() as captured:
                sns.histplot(
                    data = visualization_df,
                    x = numerical_feature,
                    hue = categorical_feature, 
                    stat="count", 
                    multiple="stack",
                    bins=age_bins if numerical_feature == 'Age' else 'auto'
                    )
                plt.xlim(xmin=0)
                plt.ylim(ymin=0)
                plt.ylabel('No. customers')
                plt.title('Distribution of {}'.format(numerical_feature.lower()))
                plt.tight_layout()
            plt.show()
            plt.close()
            
    for feature_set in combinations(categorical_features, 2):
        if len(visualization_df[feature_set[0]].cat.categories) <= len(visualization_df[feature_set[1]].cat.categories):
            hue = feature_set[0]
            x = feature_set[1]
        else:
            hue = feature_set[1]
            x = feature_set[0]
        sns.countplot(
            data = visualization_df,
            x = x,
            hue = hue, 
            dodge = True
        )
        plt.ylim(ymin=0)
        plt.ylabel('No. customers')
        plt.title('Distribution of {}'.format(categorical_feature.lower()))
        plt.tight_layout()
        plt.show()
        plt.close()
        
def plot_boxplots(visualization_df):
    '''
    Plot boxplots for all combinations of numerical features and categorical features
    
    Parameters
    ----------
    visualization_df : pandas.core.frame.DataFrame
        DataFrame to visualize.
    '''
    
    from itertools import combinations
    
    numerical_features = list(visualization_df.select_dtypes(exclude=['object', 'category']).columns)
    categorical_features = list(visualization_df.select_dtypes(include=['object', 'category']).columns)
    
    for feature_set in combinations(categorical_features, 2):
        if len(visualization_df[feature_set[0]].cat.categories) <= len(visualization_df[feature_set[1]].cat.categories):
            hue = feature_set[0]
            categorical_feature = feature_set[1]
        else:
            hue = feature_set[1]
            categorical_feature = feature_set[0]
        for numerical_feature in numerical_features:
            with io.capture_output() as captured:
                sns.boxplot(
                    data = visualization_df,
                    x = categorical_feature, 
                    y = numerical_feature, 
                    hue = hue, 
                    orient = 'v',
                    flierprops = {'marker': 'o'}
                )
                plt.title('Distribution of {}'.format(numerical_feature.lower()))
                plt.ylabel(numerical_feature)
                plt.tight_layout()
            plt.show()
            plt.close();

def plot_scatterplots(df):
    '''
    Plot scatterplots for all combinations of numerical features.
    
    Parameters
    ----------
    visualization_df : pandas.core.frame.DataFrame
        DataFrame to visualize.
    '''

    from itertools import combinations
    
    categorical_features = list(df.select_dtypes(include='category'))
    numerical_features = list(df.select_dtypes(exclude='category'))
 
    for feature_set in combinations(numerical_features, 2):
        x = feature_set[0]
        y = feature_set[1]
        for categorical_feature in categorical_features:
            with io.capture_output() as captured:
                sns.scatterplot(
                    data = df,
                    x = x,
                    y = y,
                    hue = categorical_feature, 
                    alpha = .5
                )
                plt.xlim(xmin=0)
                plt.ylim(ymin=0)
                plt.ylabel(ylabel=y)
                plt.title(label='Distribution of {} vs. {}'.format(x.lower(), y.lower()))
                plt.tight_layout()
            plt.show()
            plt.close()
        
def plot_residuals(residuals):
    with io.capture_output() as captured:
        sns.scatterplot(
            data=residuals,
            x='Observations', 
            y='Standardized residuals',
            hue='Split',
            alpha=.5,
            s = 10
        )
        plt.xlim(xmin=0)
        plt.ylabel(ylabel='Observations')
        plt.ylabel(ylabel='Standardized residuals')
        plt.title('Residuals')
        plt.tight_layout()
    plt.show()
    plt.close()
    
