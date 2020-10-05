import statsmodels
import statsmodels.api as sm
from statsmodels.formula.api import ols


# Function chk_OLS_regression_results calculates for a given dependent variable and a dataframe of dependent variables
def run_ols_regression( df, target):
    X = df.loc[:,df.columns != target].assign(const=1)
    y = df.loc[:,df.columns == target]
    results = sm.OLS(y,X).fit() 
    print(results.summary())
    
def data_cleanup(df_merged):
    #Drop the nan zipcode records. We are using it for mapping.
    print("Before dropping nan zipcode records : ", df_merged.shape)
    df_merged = df_merged.dropna()
    print("After dropping nan zipcode records : ", df_merged.shape)
    
    #Filter out Sale Prices less than 20000.
    print("Before dropping sale price < 20000 records : ", df_merged.shape)
    df_merged = df_merged[(df_merged.SalePrice >= 20000)]
    print("After dropping sale prices 2000 : ", df_merged.shape)
    
    # Delete Merged_Key and DocumentDate. First one was use for creating this merged data file. No longer need it. 
    # No meaningful data in AirPortNoise Column. Delete it as well
    if {'Merged_Key'}.issubset(df_merged.columns): del df_merged['Merged_Key']
    if {'DocumentDate'}.issubset(df_merged.columns): del df_merged['DocumentDate']
    if {'AirportNoise'}.issubset(df_merged.columns): del df_merged['AirportNoise']
    
    # Clean up 'DaylightBasement' 
    df_merged.replace({'DaylightBasement': {'n':'N','y': 'Y', ' ':'X'}}, inplace=True)

    # Clean up Stories - some have Harry Potter like 1.51 stories.
    df_merged.replace({'Stories': {1.51:1.5}}, inplace=True)
    df_merged = df_merged[df_merged['SalePrice'] < 30000000]
    df_merged.shape
    
    # explore the data
    print("\n\nExploring merged data file:\n",df_merged.describe())

    return df_merged

def data_correlation(df_merged):
    # First, check the correlation between the predicted('SalePrice')and others
    corr = df_merged.corr()['SalePrice']
    print("\n\nSale Price Correlation:\n", corr.sort_values(ascending=False))  
    
    # Next, correlation matrix for all factors
    corr = df_merged.corr()
    return corr
