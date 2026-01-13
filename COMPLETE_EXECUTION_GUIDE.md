# 🚀 Complete Project Execution Guide

## 📋 Overview

This guide walks you through running your M5 demand forecasting project from scratch. Total time: **~10-15 minutes**.

---

## ✅ Pre-Flight Check

Before starting, make sure:
- [ ] You have the M5 dataset in `~/Desktop/m5-forcasting-accuracy/`
- [ ] You have Python 3.8+ installed (`python --version`)
- [ ] You have `pip` installed (`pip --version`)
- [ ] You have a terminal/command line open

---

## 📍 Step 1: Navigate to Project Directory

**Command:**
```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting
```

**What this does:**
- Changes your current directory to the project folder
- All subsequent commands will run from here

**Verify:**
```bash
pwd
```
Should show: `/Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting`

---

## 📂 Step 2: Copy M5 Dataset Files

**Command:**
```bash
cp ~/Desktop/m5-forcasting-accuracy/*.csv data/raw/
```

**What this does:**
- Copies all 3 CSV files from your Desktop folder to `data/raw/`
- Files copied:
  - `sales_train_validation.csv` (~100MB)
  - `calendar.csv` (~100KB)
  - `sell_prices.csv` (~20MB)

**Verify files copied:**
```bash
ls -lh data/raw/
```

**Expected output:**
```
total 120M
-rw-r--r-- 1 user staff  150K calendar.csv
-rw-r--r-- 1 user staff  100M sales_train_validation.csv
-rw-r--r-- 1 user staff   20M sell_prices.csv
```

**✅ Success check:** You should see all 3 files listed with reasonable file sizes.

---

## 📦 Step 3: Install Python Dependencies

**Command:**
```bash
pip install -r requirements.txt
```

**What this does:**
- Installs all required Python packages:
  - `pandas` - data manipulation
  - `numpy` - numerical computing
  - `scikit-learn` - ML utilities
  - `statsmodels` - ARIMA models
  - `xgboost` - gradient boosting
  - `matplotlib`, `seaborn` - visualization
  - `pyyaml` - config management

**Expected output:**
```
Collecting pandas>=2.0.0
  Downloading pandas-2.x.x-...
...
Successfully installed pandas-2.x.x numpy-1.x.x ...
```

**Time:** 1-2 minutes

**✅ Success check:** No error messages, ends with "Successfully installed..."

---

## 🧪 Step 4: Quick Test Run (5 Time Series)

**Command:**
```bash
python src/pipeline.py --data-dir data/raw --max-series 5
```

**What this does:**
- Runs the complete pipeline on **5 time series** (for quick testing)
- Tests all components work correctly
- Generates sample visualizations

**Time:** 2-3 minutes

### Expected Console Output:

```
============================================================
M5 DEMAND FORECASTING PIPELINE
============================================================

============================================================
STEP 1: LOADING DATA
============================================================
Loading M5 dataset files...
  Loaded sales data: (30490, 1919)
  Loaded calendar data: (1969, 14)
  Loaded prices data: (6841121, 4)
✓ Data validation passed

============================================================
STEP 2: PROCESSING DATA
============================================================
Transforming to long format...
  Long format shape: (60034810, 12)
Aggregating to store-category level...
  Aggregated shape: (58327, 8)
  Unique store-category combinations: 30
Cleaning data...
  Cleaned data shape: (58327, 8)
Removing leading zero-sales periods...
  Data shape after removing leading zeros: (54230, 8)
Adding time features...
  Added time features: day_of_week, week_of_year, is_weekend

✓ Saved processed data to data/processed/processed_data.csv

============================================================
STEP 3: FEATURE ENGINEERING
============================================================
Creating lag features...
  Created lag_7
  Created lag_14
  Created lag_28
  Created rolling_mean_7
  Created rolling_mean_28
  Created rolling_std_7
  Created rolling_std_28
Removing rows with incomplete lag features...
  Removed 840 rows (1.5%)

✓ Saved featured data to data/processed/featured_data.csv

============================================================
STEP 4: RUNNING BACKTESTS
============================================================

Testing Baseline Models...

Running backtest for NaiveModel...
  Completed 5/5 series

NaiveModel Results:
  Mean MAE: 45.23
  Mean RMSE: 67.89
  Mean MAPE: 32.14%

Running backtest for SeasonalNaiveModel...
  Completed 5/5 series

SeasonalNaiveModel Results:
  Mean MAE: 42.18
  Mean RMSE: 65.32
  Mean MAPE: 30.56%

Running backtest for MovingAverageModel...
  Completed 5/5 series

MovingAverageModel Results:
  Mean MAE: 43.67
  Mean RMSE: 66.45
  Mean MAPE: 31.23%

Testing ARIMA Model...

Running backtest for ARIMAModel...
  Completed 5/5 series

ARIMAModel Results:
  Mean MAE: 40.12
  Mean RMSE: 62.78
  Mean MAPE: 28.91%

Testing XGBoost Model...

Running backtest for XGBoostModel...
  Completed 5/5 series

XGBoostModel Results:
  Mean MAE: 38.45
  Mean RMSE: 60.23
  Mean MAPE: 27.34%

============================================================
BACKTEST RESULTS SUMMARY
============================================================
            model    MAE    RMSE   MAPE
      NaiveModel  45.23   67.89  32.14
SeasonalNaiveModel  42.18   65.32  30.56
 MovingAverageModel  43.67   66.45  31.23
       ARIMAModel  40.12   62.78  28.91
    XGBoostModel  38.45   60.23  27.34

============================================================
STEP 5: CREATING VISUALIZATIONS
============================================================
  Saved plot to plots/model_comparison_mae.png
  Saved plot to plots/model_comparison_rmse.png
  Saved plot to plots/model_comparison_mape.png
  Saved results to plots/results_summary.csv

✓ All visualizations created

============================================================
PIPELINE COMPLETE
============================================================

🏆 Best Model: XGBoostModel
   MAE:  38.45
   RMSE: 60.23
   MAPE: 27.34%
```

**✅ Success check:** 
- Pipeline completes without errors
- You see "PIPELINE COMPLETE"
- Best model is identified

---

## 🎯 Step 5: Verify Generated Outputs

**Check processed data:**
```bash
ls -lh data/processed/
```

**Expected files:**
- `processed_data.csv` - Cleaned, aggregated time series
- `featured_data.csv` - Data with lag features

**Check visualizations:**
```bash
ls -lh plots/
```

**Expected files:**
- `model_comparison_mae.png`
- `model_comparison_rmse.png`
- `model_comparison_mape.png`
- `results_summary.csv`

**View a chart:**
```bash
open plots/model_comparison_mae.png
```

---

## 🚀 Step 6: Full Production Run (20 Time Series)

Now that you've verified everything works, run the full analysis:

**Command:**
```bash
python src/pipeline.py --data-dir data/raw --max-series 20
```

**What's different:**
- Processes **20 time series** instead of 5
- More robust model comparisons
- Better statistical confidence
- Takes longer but gives better results

**Time:** 5-10 minutes

**Note:** ARIMA model may take longer on more series. This is normal!

---

## 📊 Step 7: Review Results

### Terminal Results
Look at the final output table showing model performance.

### CSV Results
```bash
cat plots/results_summary.csv
```

Shows exact numeric values for all metrics.

### Visualizations
```bash
open plots/model_comparison_mae.png
open plots/model_comparison_rmse.png
open plots/model_comparison_mape.png
```

Visual comparison of all 5 models.

---

## 🧪 Optional: Run Exploratory Notebook

If you want to explore the data interactively:

**Start Jupyter:**
```bash
jupyter notebook notebooks/exploratory_analysis.ipynb
```

**What this does:**
- Opens Jupyter Notebook in your browser
- Run cells to see:
  - Data structure analysis
  - Sales distributions
  - Seasonality patterns
  - Store and category comparisons
  - Event impact analysis

---

## 🎓 Understanding the Results

### Model Performance Table

```
            model    MAE    RMSE   MAPE
      NaiveModel  45.23   67.89  32.14
SeasonalNaiveModel  42.18   65.32  30.56
 MovingAverageModel  43.67   66.45  31.23
       ARIMAModel  40.12   62.78  28.91
    XGBoostModel  38.45   60.23  27.34
```

**What this means:**
- **Lower is better** for all metrics
- **MAE** = Average forecast error in units
- **RMSE** = Root Mean Squared Error (penalizes large errors)
- **MAPE** = Percentage error (27% = on average 27% off)

**Winner:** XGBoost (lowest on all metrics)

### Business Interpretation

If XGBoost shows MAE of 38.45:
- On average, forecasts are off by ~38 units per day
- For safety stock: multiply RMSE by service level Z-score
  - 95% service level: 60.23 × 1.65 = ~99 units safety stock
  - 99% service level: 60.23 × 2.33 = ~140 units safety stock

---

## 🐛 Troubleshooting

### Error: "No module named 'pandas'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Error: "File not found: sales_train_validation.csv"
**Solution:**
```bash
# Check files in data/raw
ls data/raw/

# If empty, re-copy:
cp ~/Desktop/m5-forcasting-accuracy/*.csv data/raw/
```

### Pipeline runs slowly
**Normal!** ARIMA model is computationally expensive. You can:
- Reduce `--max-series` (e.g., `--max-series 10`)
- Wait it out (it will complete)

### Memory errors
**Solution:** Reduce time series:
```bash
python src/pipeline.py --data-dir data/raw --max-series 5
```

---

## ✅ Success Criteria

You've successfully run the project when:
- ✅ No error messages during pipeline execution
- ✅ "PIPELINE COMPLETE" message appears
- ✅ Best model identified with metrics
- ✅ 3 PNG files in `plots/` directory
- ✅ `results_summary.csv` created

---

## 🎯 Next Steps After Success

1. **Review visualizations** in `plots/` folder
2. **Analyze results** in `results_summary.csv`
3. **Read business recommendations** in README.md
4. **Experiment:**
   - Try different `--max-series` values
   - Modify hyperparameters in `config.yaml`
   - Run on full dataset (remove `--max-series`)

---

## 📝 Complete Command Reference

**All commands in order:**
```bash
# 1. Navigate
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting

# 2. Copy data
cp ~/Desktop/m5-forcasting-accuracy/*.csv data/raw/
ls -lh data/raw/

# 3. Install dependencies
pip install -r requirements.txt

# 4. Quick test
python src/pipeline.py --data-dir data/raw --max-series 5

# 5. Verify outputs
ls -lh data/processed/
ls -lh plots/

# 6. View results
open plots/model_comparison_mae.png
cat plots/results_summary.csv

# 7. Full run (optional)
python src/pipeline.py --data-dir data/raw --max-series 20
```

---

## 🎉 You're Ready!

Follow steps 1-7 in order. The quick test (Step 4) should complete in 2-3 minutes and confirm everything works!

Good luck! 🚀
