# PMFBY-Agricultural-Crop-Insurance-project
## Problem Definition & Objectives

Agricultural production in India is subject to substantial yield risks driven by climatic variability. The Pradhan Mantri Fasal Bima Yojana (PMFBY) and Restructured Weather Based Crop Insurance Scheme (RWBCIS) serve as fiscal stabilization mechanisms to mitigate farmer income volatility. However, managing these programs requires precise tracking of state and central government subsidy commitments, risk exposure across crop types, and regional variation in indemnity coverage.

The objective of this project is to process and analyze multi-season transaction records from PMFBY to evaluate fiscal liabilities, test distribution variances across insurance providers and crop categories, and construct time-series forecasting models to project state-level subsidy commitments.

## Technical Solution & Implementation Architecture

```
                                  [ Raw PMFBY CSV Dataset ]
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │    Module 1: Data Ingestion     │
                             │        (data_loader.py)         │
                             └─────────────────────────────────┘
                                              │
                                              ▼
                             ┌─────────────────────────────────┐
                             │  Module 2: Cleaning & Feature   │
                             │     Engineering (cleaner.py)    │
                             └─────────────────────────────────┘
                                              │
                       ┌──────────────────────┴──────────────────────┐
                       ▼                                             ▼
       ┌───────────────────────────────┐             ┌───────────────────────────────┐
       │     Module 3: Visualization   │             │   Module 4: Statistics &      │
       │      (eda_visualizer.py)      │             │   Forecasting (forecaster.py) │
       └───────────────────────────────┘             └───────────────────────────────┘
                       │                                             │
                       ▼                                             ▼
         [ Multi-Panel Plot Outputs ]                  [ Statistical Tests & ARIMA ]

```
Execution Feasibility & System Requirements

* **Runtime Environment:** Python 3.10+
* **Core Libraries:** `pandas`, `numpy`, `scipy`, `statsmodels`, `matplotlib`, `seaborn`
* **Hardware Requirement:** Standard x86_64 CPU (4 cores, 8 GB RAM); GPU acceleration is not required.
* **Execution Time:** Complete pipeline run execution (loading, cleaning, testing, visualization, and fitting) completes in $< 30$ seconds on standard hardware.
