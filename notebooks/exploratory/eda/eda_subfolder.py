import os
import pandas as pd
import numpy as np
import sys

# A function named parse_year(df, year) that takes a dataframe as the input.
# It takes in a dataframe, looks for relevant columns, and then keeps the rows that
# are in the year 2019.
def parse_year(df, year):
    if 'DocumentDate' in df.columns:
        df = df[pd.to_datetime(df['DocumentDate']).dt.year == year ]
        df.loc[:,'DocumentDate'] = str(year)
        return df
    
# Funtion to pad zeros to Major, Minor columns, if the length is less than 
# Major: Column 0; Minor: Column 1
def pad_zeros_tokey(df):
    df['Minor'] = df.Minor.astype(str).str.pad(4,fillchar='0')
    df['Major'] = df.Major.astype(str).str.pad(6,fillchar='0')
    return df

#Combine Major+Minor in one column'Merged_Key' and drop Major, Minor columns
def merge_keys (df):
    df['Merged_Key'] = df['Major'].map(str) + df['Minor'].map(str)
    df_t = df.pop('Merged_Key')
    df.insert(0, 'Merged_Key', df_t)
    del df['Major'], df['Minor']
    return df

    
# Data File: EXTR_RPSale.csv 
#Table: EXTR_RPSale 
#Keys: Major, Minorf
#Selected Columns ['Major', 'Minor', 'DocumentDate', 'SalePrice', 'PropertyType',
#       'PrincipalUse', 'PropertyClass']
# Filters:
#     1) Select only specified 'year' data
#.    2) If 'SalesPrice' is 0, drop the records
def get_sales(year=2019):
    df = pd.read_csv("../data/EXTR_RPSale.csv", encoding = "ISO-8859-1", low_memory=False)

    # Filter the following columns from EXTR_RPsale table
    cols = list(df.columns)
    df = df[cols[1:5] + cols[14:16] + cols[22:23]]
    
    #Convert mm/dd/yyyy to yyyy for further filtering
    df = parse_year(df,year)
    
    #Drop zero SalePrice records
    df = df[df['SalePrice'] != 0 ]
    
    #Pad zeros to keys
    df = pad_zeros_tokey(df)
    
    #Combine Major+Minor in one column'Merged_Key' and drop Major, Minor columns
    df = merge_keys(df)
    print("Sales file read....", df.shape)   
    return df

#Data File: EXTR_Parcel.csv
#Table: EXTR_Parcel
#Keys: Major, Minor
# Selected Columns ['Major', 'Minor', 'PropType', 'Area', 'SubArea', 'SqFtLot',
#       'WaterSystem', 'SewerSystem', 'Access', 'SeattleSkyline',
#       'LakeWashington', 'LakeSammamish', 'SmallLakeRiverCreek', 'OtherView',
#       'WfntLocation', 'WfntFootage', 'WfntBank', 'WfntPoorQuality',
#       'WfntRestrictedAccess', 'WfntAccessRights', 'WfntProximityInfluence',
#       'TidelandShoreland', 'TrafficNoise', 'AirportNoise', 'PowerLines',
#       'OtherNuisances']
def get_parcels():
    df = pd.read_csv('../data/EXTR_Parcel.csv', encoding = "ISO-8859-1", low_memory=False)
    
    # Filter the following columns from EXTR_Parcel table
    cols = list(df.columns)
    df = df[cols[:2] + cols[10:13] + cols[15:16] + cols[21:25] + cols[35:36]   + cols[37:49] + cols[50:54]] 
    
    #Pad zeros to keys
    df = pad_zeros_tokey(df)
    
#     # Filter KING County only
#     df = df[df['DistrictName'].str.contains('KING', na=False)]
#     print( "After filtering KING county rows", df.shape)
    
    # Filter Proptype R:Residential; K:Condominium
    df = df[(df['PropType'] == 'R') | (df['PropType'] == 'K')]
    print("Parcel file read....", df.shape)   
    
    #Combine Major+Minor in one column'Merged_Key' and drop Major, Minor columns
    df = merge_keys(df)
    return df

#Data File: EXTR_ResBldg.csv
#Table: EXTR_ResBldg
#Keys: Major, Minor
# Selected Columns ['Major', 'Minor', 'BldgNbr', 'NbrLivingUnits', 'Address',
#       'BuildingNumber', 'ZipCode', 'Stories', 'SqFt1stFloor', 'SqFtHalfFloor',
#       'SqFt2ndFloor', 'SqFtUpperFloor', 'SqFtUnfinFull', 'SqFtUnfinHalf',
#       'SqFtTotLiving', 'SqFtTotBasement', 'SqFtFinBasement',
#       'SqFtGarageAttached', 'DaylightBasement', 'SqFtOpenPorch',
#       'SqFtEnclosedPorch', 'SqFtDeck', 'HeatSystem', 'Bedrooms',
#       'BathHalfCount', 'Bath3qtrCount', 'BathFullCount', 'FpSingleStory',
#       'FpMultiStory', 'YrRenovated', 'PcntComplete'],

def get_resBldg():
    df = pd.read_csv('../data/EXTR_ResBldg.csv', encoding = "ISO-8859-1", low_memory=False)

    # Filter the following columns from EXTR_ResBldg table
    cols = list(df.columns)
    df = df[cols[:6]  + cols[11:13] + cols[15:24] + cols[26:32] + cols[35:41] +  cols[44:46]] 
    
    #Pad zeros to keys
    df = pad_zeros_tokey(df)
    
    #Combine Major+Minor in one column'Merged_Key' and drop Major, Minor columns
    df = merge_keys(df)
    
    print("ResBldg file read....", df.shape)     
    return df

#Data File: EXTR_LookUp.csv
#Table: EXTR_LookUp
#Keys: LUType, LUItem
# Selected Columns ['LUType', 'LUItem', 'LUDescription']
def get_lookup():
    df = pd.read_csv('../data/EXTR_LookUp.csv', encoding = "ISO-8859-1", low_memory=False)
 
    return df

#Read and return a LookUp description for a given LUType and LUItem
def get_ludescription(df, type, item):
    return df[type][item]

#Data File: EXTR_UnitBreakdown.csv
#Table: EXTR_UnitBreakdown
#Keys: Major, Minor
# All columns (['Major', 'Minor', 'UnitTypeItemId', 'NbrThisType', 'SqFt', 'NbrBedrooms', 'NbrBaths'],
def get_unitbreakdown():
    df = pd.read_csv('../data/EXTR_UnitBreakdown.csv', encoding = "ISO-8859-1", low_memory=False)
    
    #Pad zeros to key
    df = pad_zeros_tokey(df)
    
    #Combine Major+Minor in one column'Merged_Key' and drop Major, Minor columns
    df = merge_keys(df)
    
    return df

# #Function: create_consolidated
# #Table: EXTR_UnitBreakdown
# #Keys: Major, Minor
# # All columns (['Major', 'Minor', 'UnitTypeItemId', 'NbrThisType', 'SqFt', 'NbrBedrooms', 'NbrBaths'],

def consolidate_data(year=2019, create=False):
    if os.path.isfile('../data/consolidated.csv') and (create==False):
         df_merged = pd.read_csv('../data/consolidated.csv', encoding = "ISO-8859-1", low_memory=False)
    else:           
        # get read data from multiple csv files and create one consolidated data file after extracting year understudy and cleanup.
        df_sales = get_sales(year)
        df_parcels = get_parcels()
        df_resbldg = get_resBldg()
        df_unitbreakdown = get_unitbreakdown()
        df_lookup = get_lookup()
    
        #Merge df_sales, df_parcels, df_resbldg on keys Major and Minor
        print("Merging data started....")
        df_merged = df_sales
        df_merged = df_merged.merge(df_parcels, on=['Merged_Key'],  how='inner')
        df_merged = df_merged.merge(df_resbldg, on=['Merged_Key'],  how='inner')          

        df_merged.to_csv ('../data/consolidated.csv', index = False, header=True)
        print("Merging data ....done")        
    
    return df_merged
        

# using label encoding, takes the categorical columns in a dataframe and turn them into numeric ones and returns a dataframe
# inputs: a dataframe, and a boolean keep
# setting it to True will keep the old categorical column, setting it to False will delete it

def dummying_df(df, keep = True):
    cols = df.select_dtypes(include = 'object').columns
    label_encoder = LabelEncoder()
    for col in cols:
        status_labels = label_encoder.fit_transform(df[f"{col}"])
        df[f"{col}_Encoded"] = status_labels
        if keep == False: df.drop(columns = [col], inplace = True, errors = 'ignore')
    return df