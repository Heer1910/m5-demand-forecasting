"""
Data loader for M5 Forecasting dataset.
Loads raw CSV files and performs basic validation.
"""
import os
import pandas as pd
from typing import Tuple


class M5DataLoader:
    """Loads M5 dataset files from disk."""
    
    def __init__(self, data_dir: str):
        """
        Initialize the data loader.
        
        Args:
            data_dir: Path to directory containing M5 CSV files
        """
        self.data_dir = data_dir
        
    def load_all(self) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Load all M5 dataset files.
        
        Returns:
            Tuple of (sales_df, calendar_df, prices_df)
        """
        print("Loading M5 dataset files...")
        
        # Load sales data
        sales_path = os.path.join(self.data_dir, "sales_train_validation.csv")
        if not os.path.exists(sales_path):
            raise FileNotFoundError(f"Sales file not found: {sales_path}")
        sales_df = pd.read_csv(sales_path)
        print(f"  Loaded sales data: {sales_df.shape}")
        
        # Load calendar data
        calendar_path = os.path.join(self.data_dir, "calendar.csv")
        if not os.path.exists(calendar_path):
            raise FileNotFoundError(f"Calendar file not found: {calendar_path}")
        calendar_df = pd.read_csv(calendar_path)
        print(f"  Loaded calendar data: {calendar_df.shape}")
        
        # Load prices data
        prices_path = os.path.join(self.data_dir, "sell_prices.csv")
        if not os.path.exists(prices_path):
            raise FileNotFoundError(f"Prices file not found: {prices_path}")
        prices_df = pd.read_csv(prices_path)
        print(f"  Loaded prices data: {prices_df.shape}")
        
        # Basic validation
        self._validate_data(sales_df, calendar_df, prices_df)
        
        return sales_df, calendar_df, prices_df
    
    def _validate_data(self, sales_df: pd.DataFrame, 
                      calendar_df: pd.DataFrame,
                      prices_df: pd.DataFrame) -> None:
        """Validate loaded data has expected structure."""
        
        # Check sales columns
        required_sales_cols = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
        for col in required_sales_cols:
            if col not in sales_df.columns:
                raise ValueError(f"Missing required column in sales data: {col}")
        
        # Check calendar columns
        required_calendar_cols = ['date', 'd', 'wday', 'month', 'year']
        for col in required_calendar_cols:
            if col not in calendar_df.columns:
                raise ValueError(f"Missing required column in calendar data: {col}")
        
        # Check prices columns
        required_prices_cols = ['store_id', 'item_id', 'wm_yr_wk', 'sell_price']
        for col in required_prices_cols:
            if col not in prices_df.columns:
                raise ValueError(f"Missing required column in prices data: {col}")
        
        print("✓ Data validation passed")
