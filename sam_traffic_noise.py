#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import necessary functions
import os
import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.diagnostic import linear_rainbow, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

# import custom functions for data selection (eda_subfolder identical to eda, filepaths adjusted for use in eda folder)
from eda.eda import *
print(os.getcwd())
from sklearn.preprocessing import OneHotEncoder


# In[2]:


# NOTE: Year = year for analysis; create: False(read merged file created before)/True(create a merged file)
# Returns df_merged with selected columns from each file
df_merged = consolidate_data(year=2019, create=False)

def maj_min(df, drop=True):
    try:
        df.insert(0, 'Major+Minor', df.Major.astype(str) + df.Minor.astype(str))
        if drop==True:
            df.drop(['Major', 'Minor'], axis=1, inplace=True)
    except:
        print('columns missing')

    return df

# Filter data, return dataframe of "strong correlations", greater than specified decimal percentage
def df_filter(min_percent=0.12):
    #convert to decimal percent if necessary
    if min_percent > 1:
        min_percent = min_percent/100
    # create list of columns with correlations greater than a given percentage
    corr = df_merged.corr()
    strong_corrs = []
    for key, value in dict(corr.SalePrice).items():
        if abs(value) > min_percent:
            strong_corrs.append(key)

    # create dataframe of strongly correlated column
    df_strong_corr = df_merged.drop(df_merged.columns.difference(strong_corrs), 1, inplace=False).copy()
    df_strong_corr

    df_strong_corr.sort_values('SalePrice')

    return df_strong_corrs

# Creates heatmap, return heatmap
def create_heatmap():
    # create heatmap for selected data
    mask = np.triu(np.ones_like(corr, dtype=np.bool))
    fig1, ax1 = plt.subplots(figsize=(15,15))
    return sns.heatmap(corr,mask=mask, ax=ax1)


# Create dataframe of given columns (nuisance columns excluding airport noise)
def create_df_noise():
    noise_cols = ['SalePrice', 'TrafficNoise', 'PowerLines', 'OtherNuisances']

    #create dataframe of strongly correlated column
    df_noise = df_merged.drop(df_merged.columns.difference(noise_cols), 1, inplace=False).copy()

    # filter categories
    for cat in noise_cols:
        if cat != 'SalePrice':
            unique_values = df_merged[cat].unique()
            print(cat, ': ', unique_values)

    return df_noise


# Create df of chosen predictors, n samples
n = 10000
noise_sample = df_noise.sample(n).dropna().copy()

# some chosen predictors are binary-categorical, convert "Y/N" to "1/0"
for pred in noise_sample:
    # convert all numeric values to floats
    try:
        noise_sample[pred] = noise_sample[pred].astype(int)
        
    # if value is non-numeric, convert to numeric
    except:
        for i in range(len(noise_sample[pred])):
            
            if str(noise_sample[pred].iloc[i]) == 'Y':
                noise_sample[pred].iloc[i] = 1
            
            elif str(noise_sample[pred].iloc[i]) == 'N':
                noise_sample[pred].iloc[i] = 0
            
            else:
                print('Value unaccounted for.')
                
# get saleprice samples
target = noise_sample.SalePrice.copy()

# preds = noise_sample.drop('SalePrice', axis=1, inplace=False)


# In[26]:


noise_sample.head()





noise_plot = sns.pairplot(noise_sample)
plt.tight_layout()

#returns one hot encoded graph of noise data effect on sale price.
# default sample size for onehotencoding "n" is 1000
# Take *kwargs pp_plot and hmap, returns pairplot and/or heat map if set to true
def one_hot_dataframe(n=1000, pp_plot=False, hmap=False):
    # Use ohe to analyze Traffic Noise Nuisance
    ohe = OneHotEncoder(drop='first', sparse=False)
    df_trafficnoise = pd.DataFrame(ohe.fit_transform(df_merged[['TrafficNoise']]))
    df_trafficnoise.columns = list(ohe.get_feature_names())
    df_trafficnoise.index = df_merged.index
    df_trafficnoise.to_dict()
    df_trafficnoise.rename(columns={'x0_1': 'Traffic_Noise_Level_1', 'x0_2': 'Traffic_Noise_Level_2', 'x0_3': 'Traffic_Noise_Level_3'}, inplace=True)
    traffic_noise_dict = df_trafficnoise.to_dict()
    merged_dict = df_merged.to_dict()

    for key, value in traffic_noise_dict.items():
        merged_dict[key] = value

    df_trafficnoise = pd.DataFrame(merged_dict)

    #define columns for oneHotEncoding
    df_ohe_cols = ['SalePrice', 'PowerLines', 'OtherNuisances', 'Traffic_Noise_Level_1', 'Traffic_Noise_Level_2', 'Traffic_Noise_Level_3']

    #Create DF of remaining columns
    df_ohe_drop_cols = list(list(set(list(df_trafficnoise.columns))-set(df_ohe_cols)))

    df_ohe = df_trafficnoise.drop(df_ohe_drop_cols, axis=1)

    # drop outliers
    df_ohe = df_ohe[df_ohe.SalePrice < 1000000]
    df_ohe = df_ohe[df_ohe.SalePrice > 10000]

    if pplot = True:
        sns.pairplot(df_ohe.sample(1000), kind='reg')

    if heat_map = True:
        corr = df_ohe.corr()
        mask = np.triu(np.ones_like(corr, dtype=np.bool))
        fig1, ax1 = plt.subplots(figsize=(15,15))
        sns.heatmap(corr,mask=mask, ax=ax1)

    #create sample
    ohe_sample = df_ohe.sample(n)

    noise_pred_list = ['PowerLines', 'OtherNuisances', 'Traffic_Noise_Level_1', 'Traffic_Noise_Level_2', 'Traffic_Noise_Level_3']

    for noise_type in noise_pred_list:
        formula = f'SalePrice ~ {noise_type}'
        ols_model = ols(formula=formula, data=ohe_sample)
        print(f'\n\n\nSummary for {noise_type}')
        print(ols_model.fit().summary())

    formula = 'SalePrice ~ Traffic_Noise_Level_1'
    ols_model = ols(formula=formula, data=ohe_sample)
    ols_model.fit().summary()

    # create dfs for traffic no traffic
    df_traff1_0 = df_ohe[df_ohe.Traffic_Noise_Level_1 == 0]
    df_traff1_1 = df_ohe[df_ohe.Traffic_Noise_Level_1 == 1]
    df_traff2_0 = df_ohe[df_ohe.Traffic_Noise_Level_2 == 0]
    df_traff2_1 = df_ohe[df_ohe.Traffic_Noise_Level_2 == 1]
    df_traff3_0 = df_ohe[df_ohe.Traffic_Noise_Level_3 == 0]
    df_traff3_1 = df_ohe[df_ohe.Traffic_Noise_Level_3 == 1]


    avg_10 = df_traff1_0.SalePrice.mean()
    avg_11 = df_traff1_1.SalePrice.mean()
    avg_20 = df_traff2_0.SalePrice.mean()
    avg_21 = df_traff2_1.SalePrice.mean()
    avg_30 = df_traff3_0.SalePrice.mean()
    avg_31 = df_traff3_1.SalePrice.mean()

    fig, ax = plt.subplots()
    ax = sns.barplot(x = ['Moderate', 'High', 'Extreme'], y = [avg_11, avg_21, avg_31])

    plt.xlabel('Traffic Noise')
    plt.ylabel('Average Homesale Price (USD)')
    plt.title('Influence of Traffic Noise on Homesale Prices')
    plt.savefig('reports/figures/Traffic Noise Affect.png', transparent=True, bbox_inches = "tight")

