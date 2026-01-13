# Data Setup Instructions

## 📂 Where to Copy M5 Dataset Files

Your M5 dataset needs to be copied to:
```
/Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting/data/raw/
```

## 🚀 Quick Copy Commands

If your M5 dataset is on your Desktop, run these commands in your terminal:

### Option 1: If files are directly on Desktop
```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting

# Copy the three required CSV files
cp ~/Desktop/sales_train_validation.csv data/raw/
cp ~/Desktop/calendar.csv data/raw/
cp ~/Desktop/sell_prices.csv data/raw/
```

### Option 2: If files are in a folder on Desktop (e.g., "m5-forecasting-accuracy")
```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting

# Adjust the folder name if different
cp ~/Desktop/m5-forecasting-accuracy/sales_train_validation.csv data/raw/
cp ~/Desktop/m5-forecasting-accuracy/calendar.csv data/raw/
cp ~/Desktop/m5-forecasting-accuracy/sell_prices.csv data/raw/
```

### Option 3: If files are in Downloads folder
```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting

cp ~/Downloads/sales_train_validation.csv data/raw/
cp ~/Downloads/calendar.csv data/raw/
cp ~/Downloads/sell_prices.csv data/raw/
```

## ✅ Verify Files are in Place

After copying, verify all three files are present:
```bash
ls -lh /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting/data/raw/
```

You should see:
- `sales_train_validation.csv` (largest file, ~100MB)
- `calendar.csv` (small file)
- `sell_prices.csv` (medium file)

## 🏃 Run the Pipeline

Once files are in place:
```bash
cd /Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting

# Install dependencies (if not done yet)
pip install -r requirements.txt

# Run quick test with 5 time series
python src/pipeline.py --data-dir data/raw --max-series 5

# Or run full analysis with 20 time series
python src/pipeline.py --data-dir data/raw --max-series 20
```

## 📊 Expected Output Location

After running, check:
- `data/processed/` — Processed datasets
- `plots/` — Generated visualizations
- Terminal output — Model comparison results

## 🔍 If You Need Help Finding Files

Tell me:
1. What folder name did you download the M5 dataset into?
2. Is it in Desktop, Downloads, or somewhere else?

I'll give you the exact copy commands!
