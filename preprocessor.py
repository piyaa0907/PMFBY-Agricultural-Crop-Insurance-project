import pandas as pd
import numpy as np
import config


#function to rename column names using mapping dictionary
def rename_columns(df):
    # Rename columns based on dictionary in config.py
    df_renamed = df.rename(columns=config.COLUMN_MAPPING)
    return df_renamed


#function to convert text dates into datetime and calculate duration
def convert_dates_and_duration(df):
    #check if start and end date columns exist
    if 'policyStartDate' in df.columns:
        if 'policyEndDate' in df.columns:
            #convert text dates to datetime objects
            df['policyStartDate'] = pd.to_datetime(df['policyStartDate'], errors='coerce')
            df['policyEndDate'] = pd.to_datetime(df['policyEndDate'], errors='coerce')
            
            #calculate policy active duration in days
            df['policy_duration_days'] = (df['policyEndDate'] - df['policyStartDate']).dt.days

    return df


#function to impute missing numbers using medians
def impute_missing_values(df):
    #list of monetary subsidy columns to fill
    subsidy_cols = ['farmerShareValue', 'stateShareValue', 'goiShareValue']

    #for loop iterating through each subsidy column
    for col in subsidy_cols:
        #if statement checking if the column exists in data
        if col in df.columns:
            #calculate median value of the column
            col_median = df[col].median()
            #fill missing NaN values with calculated median
            df[col] = df[col].fillna(col_median)

    return df


#function to cap extreme financial values using IQR
def cap_outliers_iqr(df, outlier_cols=config.OUTLIER_COLUMNS):
    #for loop to iterate through all outlier columns
    for col in outlier_cols:
        #if statement to check column presence
        if col in df.columns:
            #calculate 1st Quartile (25th percentile)
            q1 = df[col].quantile(0.25)
            #calculate 3rd Quartile (75th percentile)
            q3 = df[col].quantile(0.75)
            #calculate Interquartile Range
            iqr = q3 - q1

            #calculate upper and lower boundary thresholds
            lower_bound = q1 - (1.5 * iqr)
            upper_bound = q3 + (1.5 * iqr)

            #clip values exceeding bounds
            df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)

    return df


#function to calculate financial ratios
def engineer_financial_ratios(df):
    #check if all financial columns are available
    if 'farmerShareValue' in df.columns:
        if 'stateShareValue' in df.columns:
            if 'goiShareValue' in df.columns:
                #calculate Total Gross Premium (TGP)
                df['TGP'] = df['farmerShareValue'] + df['stateShareValue'] + df['goiShareValue']

                #calculate Subsidy Dependence Ratio (SDR)
                df['SDR'] = (df['stateShareValue'] + df['goiShareValue']) / df['TGP']
                df['SDR'] = df['SDR'].replace([np.inf, -np.inf], np.nan).fillna(0)

                #calculate State to Central Parity Ratio
                df['parity_ratio'] = df['stateShareValue'] / df['goiShareValue']
                df['parity_ratio'] = df['parity_ratio'].replace([np.inf, -np.inf], np.nan).fillna(0)

    return df


#master function executing all cleaning functions in sequential order
def preprocess_all(df):
    print("\nStarting Data Preprocessing...")
    df = rename_columns(df)
    df = convert_dates_and_duration(df)
    df = impute_missing_values(df)
    df = cap_outliers_iqr(df)
    df = engineer_financial_ratios(df)
    print("Data Preprocessing Completed Successfully!")
    return df