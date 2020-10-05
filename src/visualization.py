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
    sns.set_context('notebook')
    corr = df_merged.corr()
    mask = np.triu(np.ones_like(corr, dtype=np.bool))

    fig1, ax1 = plt.subplots(figsize=(11, 9))
    sns.heatmap(corr, mask=mask, ax=ax1, cmap="viridis");
    plt.savefig("./visualization/" + save_fn +".png")
    return None

def create_scatterplot_df(df_porch,save_fn):
    sns.set_context('poster')
    sns.set_context("notebook")
    fig, ax = plt.subplots(figsize=(10, 10))
    sns.scatterplot(data=df_porch, x="SqFtEnclosedPorch", y="SqFtOpenPorch")    
    plt.savefig("./visualization/" + save_fn + ".png") 
    return None

def create_scatterplot(df, x , y, save_fn):
    sns.set_context('poster')
    fig, ax = plt.subplots(figsize=(8,6))
    sns.scatterplot(data=df, x=x, y=y)    
    plt.savefig("./visualization/" + save_fn + ".png") 
    return None

def create_boxplot(df, save_fn):
    sns.set_context('poster')
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

def wfyn(w):
    if w > 0:
        return 1
    else:
        return 0

def water_front_sales(df):
    sns.set_context('poster')
    df_wf = df[['SalePrice', 'WfntLocation']].copy()
       
    df_wf['Wfntyn'] = df_wf['WfntLocation'].apply(lambda x: wfyn(x))
       
    df_w = df[df['WfntLocation'] > 0]['SalePrice'].copy()
    df_nw = df[df['WfntLocation'] == 0]['SalePrice'].copy()
    
    w_outlier = ( 3 * df_w.std() ) + df_w.mean()
    nw_outlier = ( 3 * df_nw.std() ) + df_nw.mean()
    df1 = df_wf[(df_wf['Wfntyn'] == 0) & (df_wf['SalePrice'] <= nw_outlier)]
    df2 = df_wf[(df_wf['Wfntyn'] == 1) & (df_wf['SalePrice'] <= w_outlier)]
    df_wf_cheap = df1.append(df2)
    df_wf_cheap.shape
    
    df_wf_cheap[df_wf_cheap['Wfntyn'] == 1]['SalePrice'].mean() - df_wf_cheap[df_wf_cheap['Wfntyn'] == 0]['SalePrice'].mean()

    fig, ax = plt.subplots(figsize=(10, 10))
    bar_colors = ['#aed6dc', '#ff9a8d', '#4a536b']
    x_ticks = ['Normal House', 'Waterfront House']
    y_ticks = ['$0.0 mil', '$0.2 mil', '$0.4 mil', '$0.6 mil', '$0.8 mil', '$1.0 mil', '$1.2 mil', \
               '$1.4 mil', '$1.6 mil', '$1.8 mil']
    ax = sns.barplot(data = df_wf_cheap, x = "Wfntyn", y = "SalePrice", alpha = 0.9, palette = bar_colors, ci = 95, zorder = 0)
    sns.lineplot(data = df_wf_cheap, x = 'Wfntyn', y = 'SalePrice', alpha = 1, color = bar_colors[2], zorder = 10)
    ax.set_title("Average Price Increase of a Waterfront House")
    plt.ylim(0,1800000)
    ax.set_xlabel('')
    ax.set_xticklabels(x_ticks)
    ax.set_ylabel('')
    ax.set_yticklabels(y_ticks)
    plt.show()
    figure = ax.get_figure().savefig("wf_avg_price", dpi = 400, bbox_inches = "tight")   
    plt.savefig("./visualization/Water_Front_Average_Price_increase.png") 
    
    # House Price at difference waterfront locations
    df_wf['WfntLocation_cat'] = df_wf['WfntLocation'].astype('str')
    fig, ax = plt.subplots(figsize=(10, 10))
    colors = ['#4d5198', '#daf2dc', '#81b7d2', '#ffcce7']
    x_ticks = ['0', '$0 mil','$2 mil','$4 mil','$6 mil','$8 mil', '$10 mil', '$12 mil']
    y_ticks = ['Non-Waterfront','Duwamish', 'Puget Sound', 'Ship Canal', 'Lake Wash', 'Lake Samm', 'Other Lakes', 'River/Slough']
    ax = sns.boxplot(x=df_wf['SalePrice'], y=df_wf['WfntLocation_cat'], orient ='h', \
                     showfliers = False, boxprops=dict(alpha=.8), palette = colors)
    plt.xlim(-600000,12000000)
    ax.set_title("House Price")
    ax.set_xlabel('')
    ax.set_xticklabels(x_ticks)
    ax.set_ylabel('')
    ax.set_yticklabels(y_ticks)
    figure = ax.get_figure().savefig("wf_avg_breakdown", dpi = 400, bbox_inches = "tight")
    plt.savefig("./visualization/LakeFront_Sales.png") 
    return None

def sale_tier(s, df):
    d = df['SalePrice'].describe()
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

def porch_vs_house_price (df_porch):
    sns.set_context('poster')
    df_porch['SaleTier'] = df_porch['SalePrice'].apply(lambda x: sale_tier(x, df_porch))
    x_ticks = ['0', '0.0k', '0.5k', '1.0k', '1.5k', '2.0k', '2.5k', '3.0k']
    y_ticks = ['0', '0.0k', '0.5k', '1.0k', '1.5k', '2.0k', '2.5k', '3.0k']
    colors = ['#f47a60', '#ced7d8', '#7fe7dc', '#316879']
    fig, ax = plt.subplots(figsize=(10, 10))
    ax = sns.scatterplot(data=df_porch, x="SqFtOpenPorch", y="SqFtEnclosedPorch", hue = 'SaleTier', \
                         alpha = 0.8, s=500, palette = colors)
    ax.set_title("House Price compared to Porch Area")
    plt.xlim(-90,3000)
    plt.ylim(-90,3000)
    ax.set_xlabel('Open Porch Area (SqFt)')
    ax.set_xticklabels(x_ticks)
    ax.set_ylabel('Enclosed Porch Area (SqFt)')
    ax.set_yticklabels(y_ticks)

    handles, labels = ax.get_legend_handles_labels()
    handles = [handles[4], handles[3], handles[1], handles[2]]
    labels = [labels[4], labels[3], labels[1], labels[2]]
    ax.legend(handles, labels)
    plt.savefig("./visualization/porch_vs_house_price.png") 
    
    return None

# figure = ax.get_figure().savefig("porch_porch_area", dpi = 400, bbox_inches = "tight")
    