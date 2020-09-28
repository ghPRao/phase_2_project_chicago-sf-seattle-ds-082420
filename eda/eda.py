import os
import pandas as pd
import numpy as np

## Create a function get_data(create_csv)
## If create_csv = True:
##.   create a combined file rp_cons.csv from other csv files and return a dataframe rp_cons
## If create_csv = False:
##    return a data_frame with all columns from rp_cons.csv
def get_data (create_csv):

    if create_csv == False:    
        rp_cons = pd.read_csv("data/rp_cons.csv")   
    return rp_cons
    
    df_rp_sales = get_sales()
    df_parcel = get_parcels()
    df_res_bldg  = get_resBldg()
    df_unit_breakdown = get_unit_breakdown()
    
    return df_rp_sales, df_parcel, df_res_bldg, df_unit_breakdown

# Data File: EXTR_RPSale.csv -------------------------------------------------------------
#Table: EXTR_RPSale 
#Keys: Major, Minor
#Selected Columns ['Major', 'Minor', 'DocumentDate', 'SalePrice', 'PropertyType',
#       'PrincipalUse', 'PropertyClass']

def get_sales():
    df_rp_sales = pd.read_csv('data/EXTR_RPSale.csv', encoding = "ISO-8859-1", low_memory=False)
    print("Before Filer EXTR_RPSale.csv: ", df_rp_sales.shape)

    # Filter the following columns from EXTR_RPsale table
    cols = list(df_rp_sales.columns)
    df_rp_sales = df_rp_sales[cols[1:5] + cols[14:16] + cols[22:23]]
    print("After Filer EXTR_RPSale.csv: ", df_rp_sales.shape)  
    
    return df_rp_sales

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
    df_parcel = pd.read_csv('../data/EXTR_Parcel.csv', encoding = "ISO-8859-1", low_memory=False)
    print("Before EXTR_Parcel.csv: ", df_parcel.shape)
    df_parcel.columns
    
    # Filter the following columns from EXTR_Parcel table
    cols = list(df_parcel.columns)
    df_parcel = df_parcel[cols[:2] + cols[10:13] + cols[21:25] + cols[35:36]   + cols[37:49] + cols[50:54]]  
    
    print("After Filer EXTR_Parcel.csv: ", df_parcel.shape)
    return df_parcel

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
    df_res_bldg = pd.read_csv('../data/EXTR_ResBldg.csv', encoding = "ISO-8859-1", low_memory=False)
    print("EXTR_ResBldg.csv: ", df_res_bldg.shape)

    # Filter the following columns from EXTR_ResBldg table
    cols = list(df_res_bldg.columns)
    df_res_bldg = df_res_bldg[cols[:6]  + cols[11:13] + cols[15:24] + cols[26:32] + cols[35:41] +  cols[44:46]]   
    print("After Filer EXTR_ResBldg.csv: ", df_res_bldg.shape)
    
    return df_res_bldg

#Data File: EXTR_UnitBreakdown.csv
#Table: EXTR_UnitBreakdown
#Keys: Major, Minor
# All columns (['Major', 'Minor', 'UnitTypeItemId', 'NbrThisType', 'SqFt', 'NbrBedrooms', 'NbrBaths'],
def get_unitbreakdown():
    df_unit_breakdown = pd.read_csv('../data/EXTR_UnitBreakdown.csv', encoding = "ISO-8859-1", low_memory=False)
    print("EXTR_UnitBreakdown: ", df_unit_breakdown.shape)
    
    return df_unit_breakdown