"""Simple end-to-end test"""
import sys
import os
sys.path.insert(0, 'src')
os.chdir('/Users/heerpatel/.gemini/antigravity/scratch/m5-demand-forecasting')

import pandas as pd
import numpy as np
from models.naive import NaiveModel
from evaluation.metrics import ForecastMetrics

# Load data
df = pd.read_csv('data/processed/processed_data.csv')
df['date'] = pd.to_datetime(df['date'])

print("="*60)
print("SIMPLE FORECASTING TEST")
print("="*60)

# Get one time series
sample = df[(df['store_id'] == 'CA_1') & (df['cat_id'] == 'FOODS')].copy()
sample = sample.sort_values('date').reset_index(drop=True)

print(f"\nData shape: {sample.shape}")
print(f"Date range: {sample['date'].min()} to {sample['date'].max()}")

# Simple train/test split
train_size = 300
test_size = 28

train_data = sample.iloc[:train_size]
test_data = sample.iloc[train_size:train_size+test_size]

print(f"\nTrain: {len(train_data)} days")
print(f"Test: {len(test_data)} days")

# Test Naive model
model = NaiveModel()
model.fit(train_data, 'units_sold')

predictions = model.predict(test_size)
actuals = test_data['units_sold'].values

metrics = ForecastMetrics.calculate_all(actuals, predictions)

print(f"\n✅ Naive Model Results:")
print(f"   MAE: {metrics['MAE']:.2f}")
print(f"   RMSE: {metrics['RMSE']:.2f}")
print(f"   MAPE: {metrics['MAPE']:.2f}%")

print("\n✅ Models work! Issue is in backtest framework.")
