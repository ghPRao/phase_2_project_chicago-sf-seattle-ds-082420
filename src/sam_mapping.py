#!/usr/bin/env python
# coding: utf-8

# In[1]:
# this function will import all necessary packages for data analysis and cleaning
# You have the option to omit mapping packages my setting mapping=False
def package_import(mapping=True):
    import os
    import sys

    import pandas as pd
    import geopandas as gpd

    import numpy as np

    import matplotlib.pyplot as plt
    import seaborn as sns

    import statsmodels.api as sm

    from statsmodels.formula.api import ols
    from statsmodels.stats.diagnostic import linear_rainbow, het_breuschpagan
    from statsmodels.stats.outliers_influence import variance_inflation_factor

    from collections import Counter
    import re
    import ast

    # import custom functions for data selection
    from eda.eda import *

    if mapping = True:
        # import packages for mapping
        from geopandas.tools import sjoin
        import folium
        from folium.plugins import MarkerCluster
        from folium import IFrame
        import shapely
        from shapely.geometry import Point
        import unicodedata
        import pysal as ps
        import libpysal as lps
        import mapclassify
        # for saving map
        import time
        from selenium import webdriver
        import subprocess


# In[3]:
#this function creates required dataframe, option to create csv, default to false
def create_df(create_csv=False):
    df_merged = consolidate_data(year=2019, create=create_csv)

# In[5]:
# function to load shapefiles
# return zipcode shapefile geopandas dataframe "zip_shp" and "geozips"
def load_shp():
    filename = '../data/shapefiles/Zip_Codes-shp/Zip_Codes.shp'
    zip_shp = gpd.read_file(filename)
    geo_zips = gpd.GeoDataFrame(zip_shp)
    geo_zips

    return zip_shp, geo_zips

# returns "df_merged" dataframe with geolocation data
def add_zips():
    # find all zip codes in merged dataframe (df_merged)
    merged_zips = df_merged.ZipCode.unique()

    #load latitude and longitude data

    lat_long_info = pd.read_csv('lat_long_column.csv')

    latlst = ['Latitude']
    longlst = ['Longitude']

    for i in range(len(lat_long_info.lat_long)):
        entry = lat_long_info.lat_long[i]
        entry_tuple =  ast.literal_eval(entry)
        entry_tuple = (float(entry_tuple[0]), float(entry_tuple[1]))
        latlst.append(entry_tuple[0])
        longlst.append(entry_tuple[1])

    lat = latlst[1:]
    long = longlst[1:]

    latlonpd = pd.DataFrame(data=np.array(lat), columns=['Latitude'])
    latlonpd.insert(1, column='Longitude', value=np.array(long))

    # add cleaned lat, long data to dataframe
    df_merged['Latitude'] = latlonpd.Latitude
    df_merged['Longitude'] = latlonpd.Longitude


    # create new dataframe with select columns
    df_zips = df_merged[['SalePrice', 'ZipCode', 'Latitude', 'Longitude', 'Address']].copy().dropna()

    return df_zips



# clean zipcodes, returns df with valid zipcodes
def clean_zips():
        for i in range(len(df_zips.ZipCode)):
            current_zip = df_zips.ZipCode.iloc[i]
            if current_zip == '988122':
                print('found 988122, omit extra 8')
                df_zips.ZipCode.iloc[i] = '98122'

            if current_zip == '89045':
                print('found 89045, switched to 98')
                df_zips.ZipCode.iloc[i] = '98045'

            elif len(current_zip) > 3:
                df_zips.ZipCode[i] = current_zip[:5]

            else:
                print(f'Check zip code at index {i}')
                continue
# initial number of cols
    cols_i = len(df_merged.ZipCode.unique())
    # fina number of cols
    cols_f = len(df_zips.ZipCode.unique())
    cols_diff = cols_i - cols_f
    print(f"{cols_diff} column(s) dropped due to N/A Zipcode values.")
    return df_zips

# adds column of average sale price by zip, returns "geo_zips" dataframe
def add_avg():
    # Create column of average sales by zip code
    sale_avg_b`y_zip = pd.DataFrame(df_zips.groupby('ZipCode').mean())

    # reset index
    sale_avg_by_zip.reset_index(inplace=True)


    # In[21]:


    # add column containing avg_per_zip
    for i in range(len(sale_avg_by_zip)):
        current_zip = sale_avg_by_zip.ZipCode.iloc[i]
        avg_sale = sale_avg_by_zip.SalePrice.iloc[i]
        df_zips.loc[(df_zips.ZipCode == current_zip), 'Average_by_Zipcode'] = avg_sale
        geo_zips.loc[(geo_zips.ZIPCODE == current_zip), 'Average_by_Zipcode'] = avg_sale



    # create intermediate series object needed for mapping
    series = gpd.GeoSeries(data = geo_zips.geometry, crs={'init':'epsg:4326'})

    geo_zips['geometry'] = series
    return geo_zips


#creates maps from dataframe using sample size n, and given ranges
# map populated with pins showing top, median, and bottom "n" house sale prices
#

def create_maps(n=100, marker_ranges=[10, 20, 30], marker_colors=['red', 'black', 'orange'], save_png=False):
    # create basemap centered on king county, other features to be added
    # king county location
    seattle_loc = (47.55, -122.15)

    # create sample of data, size n
    df_sample = df_zips.sample(n)

    # sort DF for purpose of finding extreme and mean values
    df_sales_sorted = df_zips.sort_values('SalePrice')

    # create additional dataframe with some outliers removed, sales below price_min
    PRICE_MIN = 50000
    df_sales_sorted = df_sales_sorted[df_sales_sorted.SalePrice > PRICE_MIN]

    # CREATE MAP
    map = folium.Map(location=seattle_loc, zoom_start=10.1, zoom_control=False, scrollWheelZoom=False, dragging=False, left='5%', width='70%', )

    # loop to create maps of each range
    for mr in marker_ranges:
        # find median value
        median = int(np.floor(len(df_sales_sorted)/2))

        # create ranges
        top = df_sales_sorted[-mr:]
        mid = df_sales_sorted[median-int(mr/2): median+int(mr/2)]
        bottom = df_sales_sorted[:mr]
        markers = [top, mid, bottom]
        # FOR LOOP TO CREATE MARKERS
        for i in range(len(markers)):
            marker = markers[i]
            for point in range(0, len(marker.Latitude)):
                folium.Marker((marker.Latitude.iloc[point], marker.Longitude.iloc[point] ) , popup=marker.SalePrice.iloc[point], icon=folium.Icon(color=marker_colors[i])).add_to(map)

        # save map(s) as .html file
        delay=5
        fn=f'reports/figures/map_range_{mr}.html'
        path=os.getcwd()
        tmpurl=f'file://{path}/{fn}'#.format(,mapfile=fn)
        map.save(fn)

        # save map(s) as png files
        if save_png = True:
            browser = webdriver.Firefox()
            browser.get(tmpurl)
            #Give the map tiles some time to load
            time.sleep(delay)
            # Create path again
            filepath=f'file://{path}/{fn}.png'
            browser.save_screenshot(filepath)
            browser.quit()