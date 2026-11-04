import pandas as pd
import config

def load_dataset(file_path=config.RAW_DATA_PATH):
    #reads the PMFBY CSV dataset into a Pandas DataFrame.
    try:
        #load the CSV file into memory
        df = pd.read_csv(file_path)
        print(f" Dataset successfully loaded! Total rows: {len(df)}, Total columns: {len(df.columns)}")
        return df
    
    except FileNotFoundError:
        print(f" Error: The file '{file_path}' was not found. Check if the filename or location is correct.")
        return None
    
    except Exception as e:
        print(f" An error occurred while reading the file: {e}")
        return None


def validate_columns(df, required_columns=config.REQUIRED_COLUMNS):
    #checks if all required financial columns exist in the loaded dataset

    #safety check: ensure a valid DataFrame was passed
    if df is None:
        print(" Error: Cannot validate columns because the DataFrame is empty.")
        return False

    #check for missing columns by comparing required list with DataFrame columns
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        print(f" Warning: Missing required columns in dataset: {missing_columns}")
        return False
    
    print(" Validation Successful: All required financial columns are present!")
    return True