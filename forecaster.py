import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
import config


#Function to execute statistical hypothesis tests on premium rates
def run_hypothesis_tests(df):
    #Check if required columns exist
    if 'premiumRate' not in df.columns or 'crop_type' not in df.columns:
        print("Missing required columns for hypothesis testing.")
        return

    print("\n--- Running Statistical Hypothesis Tests ---")

    #Create empty list to store values for each crop group
    crop_groups = []

    #For loop to extract premium rate lists grouped by crop type
    for crop_name, group_data in df.groupby('crop_type'):
        #Filter out missing values
        clean_rates = group_data['premiumRate'].dropna().values
        #If group has data, append to our list
        if len(clean_rates) > 0:
            crop_groups.append(clean_rates)

    #Check if we have at least 2 groups to compare
    if len(crop_groups) < 2:
        print("Not enough crop groups available for comparative testing.")
        return

    #Check for normality assumption using Shapiro-Wilk test
    is_normal = True
    for group in crop_groups:
        # Shapiro-Wilk requires at least 3 samples
        if len(group) >= 3:
            stat_val, p_norm = stats.shapiro(group)
            # If p-value is less than alpha, data is not normal
            if p_norm < config.ALPHA:
                is_normal = False
                break

    #Check equal variance assumption using Levene's test
    stat_val, p_levene = stats.levene(*crop_groups)
    is_homogeneous = p_levene >= config.ALPHA

    print("Normality Preserved:", is_normal)
    print("Equal Variances (Homogeneity):", is_homogeneous)

    #Select appropriate test using if-else logic
    if is_normal and is_homogeneous:
        # Run One-Way ANOVA test if assumptions hold
        f_stat, p_val = stats.f_oneway(*crop_groups)
        test_used = "One-Way ANOVA (Parametric)"
    else:
        #Run Kruskal-Wallis test if assumptions fail
        f_stat, p_val = stats.kruskal(*crop_groups)
        test_used = "Kruskal-Wallis H-Test (Non-Parametric)"

    print("\nSelected Test:", test_used)
    print("Test Statistic:", round(f_stat, 4))
    print("P-Value:", p_val)

    #Evaluate p-value against significance threshold alpha
    if p_val < config.ALPHA:
        print("Conclusion: Statistically significant difference in premium rates across crop types!")
    else:
        print("Conclusion: No statistically significant difference in premium rates across crop types.")


#Function to prepare time-series subsidy data
def prepare_subsidy_series(df):
    if 'crop_year' in df.columns and 'stateShareValue' in df.columns:
        # Group data by year and calculate yearly sum of state subsidy
        ts_data = df.groupby('crop_year')['stateShareValue'].sum()
        return ts_data
    return None


#Function to test stationarity using Augmented Dickey-Fuller (ADF) test
def check_stationarity(ts_data):
    adf_result = adfuller(ts_data.dropna())
    p_value = adf_result[1]

    print("\n--- Stationarity Test (ADF) ---")
    print("ADF P-Value:", round(p_value, 4))

    #Evaluate stationarity based on p-value
    if p_value <= config.ALPHA:
        print("Result: Time series is stationary (no differencing required).")
        return True
    else:
        print("Result: Time series is non-stationary (differencing required).")
        return False


#Function to fit ARIMA model and print evaluation metrics
def fit_arima_forecast(ts_data):
    if ts_data is None or len(ts_data) < 3:
        print("Not enough time-series data points to fit ARIMA model.")
        return

    print("\n--- Fitting Time-Series ARIMA Model ---")

    #Train ARIMA model using order from config.py
    model = ARIMA(ts_data, order=config.ARIMA_ORDER)
    model_fit = model.fit()

    #Generate model predictions for input time frame
    predictions = model_fit.predict(start=0, end=len(ts_data) - 1)

    actual = ts_data.values
    predicted = predictions.values

    #Calculate Root Mean Squared Error (RMSE)
    rmse = np.sqrt(np.mean((actual - predicted) ** 2))

    #Calculate Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual - predicted) / np.where(actual == 0, 1e-5, actual))) * 100

    print("Model Fitted: ARIMA", config.ARIMA_ORDER)
    print("Root Mean Squared Error (RMSE):", round(rmse, 2))
    print("Mean Absolute Percentage Error (MAPE):", round(mape, 2), "%")

    return model_fit