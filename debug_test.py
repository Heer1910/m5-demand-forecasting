"""Debug script to test models directly"""
import sys
sys.path.insert(0, 'src')

import pandas as pd
import numpy as np
from models.naive import NaiveModel
from models.seasonal_naive import SeasonalNaiveModel

# Load processed data
df = pd.read_csv('data/processed/processed_data.csv')
df['date'] = pd.to_datetime(df['date'])

print(f"Total data shape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nUnique store-category combos: {df.groupby(['store_id', 'cat_id']).ngroups}")

# Get first time series
first_group = df.groupby(['store_id', 'cat_id']).first().index[0]
print(f"\nTesting with: {first_group}")

sample_data = df[(df['store_id'] == first_group[0]) & (df['cat_id'] == first_group[1])].copy()
sample_data = sample_data.sort_values('date').reset_index(drop=True)

print(f"Sample data shape: {sample_data.shape}")
print(f"Date range: {sample_data['date'].min()} to {sample_data['date'].max()}")
print(f"\nFirst 5 rows:")
print(sample_data.head())
print(f"\nSample stats:")
print(sample_data['units_sold'].describe())

# Test naive model
print("\n" + "="*60)
print("Testing Naive Model")
print("="*60)

train = sample_data.iloc[:200]
test = sample_data.iloc[200:228]

print(f"Train size: {len(train)}")
print(f"Test size: {len(test)}")

model = NaiveModel()
try:
    model.fit(train, 'units_sold')
    print(f"Last value stored: {model.last_value}")
    
    predictions = model.predict(len(test))
    print(f"Predictions shape: {predictions.shape}")
    print(f"Predictions: {predictions[:5]}")
    
    actuals = test['units_sold'].values
    print(f"Actuals: {actuals[:5]}")
    
    mae = np.mean(np.abs(actuals - predictions))
    print(f"MAE: {mae}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test seasonal naive
print("\n" + "="*60)
print("Testing Seasonal Naive Model")
print("="*60)

model2 = SeasonalNaiveModel()
try:
    model2.fit(train, 'units_sold')
    print(f"Recent values stored: {model2.recent_values}")
    
    predictions = model2.predict(len(test))
    print(f"Predictions shape: {predictions.shape}")
    print(f"Predictions: {predictions[:5]}")
    
    mae = np.mean(np.abs(actuals - predictions))
    print(f"MAE: {mae}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
