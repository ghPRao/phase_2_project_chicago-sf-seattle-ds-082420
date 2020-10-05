import os
import sys

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib

def create_pairplot(df_merged, save_fn):
    sns.pairplot(df_merged);
    plt.savefig('../visualization/"+save_fn+".png')   
    return None

def create_heatmap(df_merged, save_fn):
    corr = df_merged.corr()
    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    fig1, ax1 = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, mask=mask, ax=ax1, cmap="viridis");
    plt.savefig("./visualization/" + save_fn +".png")
    return None

def create_scatterplot_df(df_porch,save_fn):
    sns.set_context("notebook")
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.scatterplot(data=df_porch, x="SqFtEnclosedPorch", y="SqFtOpenPorch")    
    plt.savefig("./visualization/" + save_fn + ".png") 
    return None

def create_scatterplot(df, x , y, save_fn):
    sns.set_context("notebook")
    fig, ax = plt.subplots(figsize=(8,6))
    sns.scatterplot(data=df, x=x, y=y)    
    plt.savefig("./visualization/" + save_fn + ".png") 
    return None

def create_boxplot(df, save_fn):
    sns.set_context("notebook")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.boxplot(df[save_fn])
    plt.savefig("./visualization/" + save_fn + ".png")
    
def sale_tier(s):
    d = df_porch['SalePrice'].describe()
    r = ''
    if s >= d['75%']:
        r = 'Luxury Housing'
    elif s >= d['50%']:
        r = 'High-End Housing'
    elif s >= d['25%']:
        r = 'Medium-End Housing'
    else:
        r = 'Low-End Housing'
    return r

