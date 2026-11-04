import os

#if file path changes or column renamed you only update it once here

#tells python where the dataset is located
RAW_DATA_PATH = "PMFBY coverage.csv"

#tells python where to save output graphs and plots
OUTPUT_DIR = "outputs"

#creates the 'outputs' folder automatically preventing FileNotFoundError
os.makedirs(OUTPUT_DIR, exist_ok=True)
#if already exists, exist_ok prevents FileExistsError


#COLUMN RENAMING MAP
#maps messy column names (with dots) to clean python names
COLUMN_MAPPING = {
    "sssyName.stateName": "state_name",
    "sssyName.year": "crop_year",
    "sssyName.seasonName": "season_name",
    "sssyName.schemeNameShort": "scheme_name",
    "level3Name": "district_name",
    "cropName": "crop_name",
    "cropType": "crop_type"
}

#REQUIRED COLUMNS FOR VALIDATION
#list of columns that must exist in your CSV for the project to run
REQUIRED_COLUMNS = [
    "sumInsured",
    "premiumRate",
    "indemnityLevel",
    "farmerShareValue",
    "stateShareValue",
    "goiShareValue"
]

#COLUMNS FOR OUTLIER CLEANING
#list of financial columns that have extreme high numbers (outliers)
OUTLIER_COLUMNS = [
    "sumInsured",
    "farmerShareValue",
    "stateShareValue",
    "goiShareValue"
]

#STATISTICAL & MODEL SETTINGS
#P-value threshold for hypothesis testing(5%)
ALPHA = 0.05

#default order (p, d, q) for time-series ARIMA forecasting
ARIMA_ORDER = (1, 1, 1)