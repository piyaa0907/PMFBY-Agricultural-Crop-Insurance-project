import config
import data_loader
import preprocessor
import eda_visualizer
import forecaster


def main():
    #master pipeline orchestrating the complete PMFBY Analytics project.
    
    print("=" * 60)
    print("  PMFBY CROP INSURANCE RISK ANALYTICS & FORECASTING PIPELINE  ")
    print("=" * 60)

    #STEP 1 & 2: DATA INGESTION & VALIDATION
    print("\n[STEP 1/5] Ingesting Raw PMFBY Dataset...")
    df_raw = data_loader.load_dataset(file_path=config.RAW_DATA_PATH)

    if df_raw is None:
        print(" Critical Error: Dataset could not be loaded. Terminating pipeline.")
        return

    print("\n[STEP 2/5] Validating Required Schema & Columns...")
    is_valid = data_loader.validate_columns(df_raw, required_columns=config.REQUIRED_COLUMNS)

    if not is_valid:
        print(" Critical Error: Required columns are missing. Terminating pipeline.")
        return

    #STEP 3: DATA PREPROCESSING & CLEANING
    print("\n[STEP 3/5] Preprocessing & Cleaning Data...")
    df_clean = preprocessor.preprocess_all(df_raw)

    #STEP 4: EXPLORATORY DATA VISUALIZATION
    print("\n[STEP 4/5] Generating Data Visualizations...")
    eda_visualizer.generate_all_plots(df_clean)

    #STEP 5: STATISTICAL TESTING & ARIMA FORECASTING
    print("\n[STEP 5/5] Executing Statistical Analytics & Forecasting...")
    
    #A. Hypothesis Testing
    forecaster.run_hypothesis_tests(df_clean)

    #B. Time-Series Subsidy Forecasting
    ts_subsidy = forecaster.prepare_subsidy_series(df_clean)
    
    if ts_subsidy is not None:
        forecaster.check_stationarity(ts_subsidy)
        forecaster.fit_arima_forecast(ts_subsidy)

    print("\n" + "=" * 60)
    print(" PIPELINE EXECUTION COMPLETE! ALL OUTPUTS SAVED TO 'outputs/' ")
    print("=" * 60)


if __name__ == "__main__":
    main()