# Quick Start Guide

## Prerequisites
You mentioned you've already downloaded the M5 dataset. Before running the pipeline, you need to place the data files in the correct location.

## Setup Steps

### 1. Copy M5 Data Files
Copy the three M5 CSV files to `data/raw/`:
```bash
cp /path/to/your/downloaded/sales_train_validation.csv m5-demand-forecasting/data/raw/
cp /path/to/your/downloaded/calendar.csv m5-demand-forecasting/data/raw/
cp /path/to/your/downloaded/sell_prices.csv m5-demand-forecasting/data/raw/
```

### 2. Install Dependencies
```bash
cd m5-demand-forecasting
pip install -r requirements.txt
```

### 3. Run Full Pipeline (Quick Test)
Test with 5 time series:
```bash
python src/pipeline.py --data-dir data/raw --max-series 5
```

### 4. Run Full Analysis
Process more time series for comprehensive results:
```bash
python src/pipeline.py --data-dir data/raw --max-series 20
```

## Expected Output

The pipeline will:
1. ✅ Load M5 data files
2. ✅ Process and aggregate to store-category level
3. ✅ Create lag features
4. ✅ Train 5 models with rolling backtesting
5. ✅ Generate visualizations in `plots/`
6. ✅ Identify best performing model

## Output Files

After running, you'll have:
- `data/processed/processed_data.csv` — Cleaned data
- `data/processed/featured_data.csv` — Data with lag features
- `plots/model_comparison_mae.png` — MAE comparison chart
- `plots/model_comparison_rmse.png` — RMSE comparison chart
- `plots/model_comparison_mape.png` — MAPE comparison chart
- `plots/results_summary.csv` — Numeric results table

## Next Steps

1. **Where is your M5 data located?** Let me know the path and I can help you copy it.
2. **Set workspace**: Consider setting `m5-demand-forecasting` as your active workspace.
3. **Run the pipeline**: Execute the commands above to test the implementation.

## Troubleshooting

**Import errors?**  
Make sure you're running from the project root: `cd m5-demand-forecasting`

**Data not found?**  
Verify files are in `data/raw/` with exact names:
- sales_train_validation.csv
- calendar.csv  
- sell_prices.csv

**Out of memory?**  
Reduce `--max-series` parameter to process fewer time series.
