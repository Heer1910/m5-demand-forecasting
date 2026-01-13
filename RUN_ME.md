# 🚀 Ready to Run - Execute These Commands

## Step 1: Copy M5 Data Files

Open your terminal and run these commands:

```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting

# Copy all CSV files from your Desktop folder
cp ~/Desktop/m5-forcasting-accuracy/*.csv data/raw/
```

## Step 2: Verify Files Copied

```bash
ls -lh data/raw/
```

You should see:
- `sales_train_validation.csv` (~100MB)
- `calendar.csv` (small)
- `sell_prices.csv` (medium)

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Run Quick Test (5 time series - ~2 minutes)

```bash
python src/pipeline.py --data-dir data/raw --max-series 5
```

## Step 5: View Results

After completion, check:
- Terminal output for model comparison
- `plots/` folder for visualizations
- `plots/results_summary.csv` for detailed metrics

## Optional: Run Full Analysis (20 time series - ~5-10 minutes)

```bash
python src/pipeline.py --data-dir data/raw --max-series 20
```

---

## 🎯 All Commands in One Block

Copy and paste this entire block:

```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting
cp ~/Desktop/m5-forcasting-accuracy/*.csv data/raw/
ls -lh data/raw/
pip install -r requirements.txt
python src/pipeline.py --data-dir data/raw --max-series 5
```

---

## ✅ Expected Output

You'll see output like:
```
============================================================
M5 DEMAND FORECASTING PIPELINE
============================================================

STEP 1: LOADING DATA
  Loaded sales data: (30490, 1919)
  ✓ Data validation passed

STEP 2: PROCESSING DATA
  Long format shape: (60034810, 12)
  Aggregated shape: (58327, 8)
  ...

STEP 4: RUNNING BACKTESTS
  Testing Baseline Models...
  NaiveModel Results:
    Mean MAE: 45.23
    ...

🏆 Best Model: XGBoostModel
   MAE:  38.45
   RMSE: 60.23
   MAPE: 27.34%
```

Results saved to `plots/` directory!
