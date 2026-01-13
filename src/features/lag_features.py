"""
Feature engineering for time series forecasting.
Creates lag features and rolling statistics.
"""
import pandas as pd
import numpy as np


class LagFeatureEngineer:
    """Creates lag-based features for time series forecasting."""
    
    def __init__(self, lag_days: list = None, rolling_windows: list = None):
        """
        Initialize feature engineer.
        
        Args:
            lag_days: List of lag days to create (e.g., [7, 14, 28])
            rolling_windows: List of rolling window sizes (e.g., [7, 28])
        """
        self.lag_days = lag_days or [7, 14, 28]
        self.rolling_windows = rolling_windows or [7, 28]
    
    def create_features(self, df: pd.DataFrame, 
                       group_cols: list,
                       target_col: str = 'units_sold') -> pd.DataFrame:
        """
        Create lag features for each time series.
        
        Args:
            df: DataFrame with time series data
            group_cols: Columns defining each time series
            target_col: Column to create lags from
            
        Returns:
            DataFrame with lag features added
        """
        print("Creating lag features...")
        df = df.copy()
        
        # Sort by group and date
        df = df.sort_values(group_cols + ['date']).reset_index(drop=True)
        
        # Create lag features
        for lag in self.lag_days:
            col_name = f'lag_{lag}'
            df[col_name] = df.groupby(group_cols)[target_col].shift(lag)
            print(f"  Created {col_name}")
        
        # Create rolling mean features
        for window in self.rolling_windows:
            col_name = f'rolling_mean_{window}'
            df[col_name] = df.groupby(group_cols)[target_col].transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=1).mean()
            )
            print(f"  Created {col_name}")
        
        # Create rolling std features
        for window in self.rolling_windows:
            col_name = f'rolling_std_{window}'
            df[col_name] = df.groupby(group_cols)[target_col].transform(
                lambda x: x.shift(1).rolling(window=window, min_periods=1).std()
            )
            print(f"  Created {col_name}")
        
        return df
    
    def get_feature_columns(self) -> list:
        """
        Get list of feature column names that will be created.
        
        Returns:
            List of feature column names
        """
        features = []
        
        # Lag features
        for lag in self.lag_days:
            features.append(f'lag_{lag}')
        
        # Rolling means
        for window in self.rolling_windows:
            features.append(f'rolling_mean_{window}')
            features.append(f'rolling_std_{window}')
        
        # Calendar features (added separately)
        features.extend(['day_of_week', 'week_of_year', 'is_weekend', 'has_event'])
        
        return features
    
    def remove_incomplete_rows(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows with NaN values in lag features.
        
        Args:
            df: DataFrame with lag features
            
        Returns:
            DataFrame with complete cases only
        """
        print("Removing rows with incomplete lag features...")
        initial_rows = len(df)
        
        # Get lag feature columns
        lag_cols = [col for col in df.columns if col.startswith('lag_') or col.startswith('rolling_')]
        
        # Drop rows with any NaN in lag features
        df = df.dropna(subset=lag_cols).reset_index(drop=True)
        
        removed_rows = initial_rows - len(df)
        print(f"  Removed {removed_rows} rows ({removed_rows/initial_rows*100:.1f}%)")
        
        return df
