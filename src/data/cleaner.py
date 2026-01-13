"""
Data cleaning and validation utilities.
"""
import pandas as pd
import numpy as np


class DataCleaner:
    """Cleans and validates time series data."""
    
    def __init__(self):
        pass
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean time series data.
        
        Args:
            df: DataFrame with time series data
            
        Returns:
            Cleaned DataFrame
        """
        print("Cleaning data...")
        df = df.copy()
        
        # Remove negative values
        if 'units_sold' in df.columns:
            negative_count = (df['units_sold'] < 0).sum()
            if negative_count > 0:
                print(f"  Removing {negative_count} negative sales values")
                df = df[df['units_sold'] >= 0]
        
        # Ensure date column is datetime
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
        
        # Sort by date
        if 'date' in df.columns:
            df = df.sort_values('date').reset_index(drop=True)
        
        print(f"  Cleaned data shape: {df.shape}")
        return df
    
    def remove_leading_zeros(self, df: pd.DataFrame, 
                            group_cols: list,
                            value_col: str = 'units_sold') -> pd.DataFrame:
        """
        Remove leading zero-sales periods for each time series.
        
        Args:
            df: DataFrame with time series data
            group_cols: Columns defining each time series
            value_col: Column containing sales values
            
        Returns:
            DataFrame with leading zeros removed
        """
        print("Removing leading zero-sales periods...")
        
        def remove_leading_zeros_group(group):
            # Find first non-zero sale
            non_zero_idx = group[group[value_col] > 0].index
            if len(non_zero_idx) == 0:
                return group.iloc[0:0]  # Return empty if all zeros
            first_sale = non_zero_idx[0]
            return group.loc[first_sale:]
        
        df = df.groupby(group_cols, group_keys=False).apply(remove_leading_zeros_group)
        df = df.reset_index(drop=True)
        
        print(f"  Data shape after removing leading zeros: {df.shape}")
        return df
    
    def validate_continuous_dates(self, df: pd.DataFrame,
                                  group_cols: list) -> bool:
        """
        Validate that dates are continuous for each time series.
        
        Args:
            df: DataFrame with date column
            group_cols: Columns defining each time series
            
        Returns:
            True if all series have continuous dates
        """
        print("Validating date continuity...")
        
        def check_continuity(group):
            dates = pd.to_datetime(group['date']).sort_values()
            date_diffs = dates.diff()[1:]
            return (date_diffs == pd.Timedelta(days=1)).all()
        
        all_continuous = df.groupby(group_cols).apply(check_continuity).all()
        
        if all_continuous:
            print("  ✓ All time series have continuous dates")
        else:
            print("  ⚠ Warning: Some time series have date gaps")
        
        return all_continuous
