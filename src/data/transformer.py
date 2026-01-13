"""
Data transformation utilities for M5 dataset.
Aggregates SKU-level data to store-category level.
"""
import pandas as pd
import numpy as np


class DataTransformer:
    """Transforms M5 data to desired aggregation level."""
    
    def __init__(self):
        pass
    
    def transform_to_long_format(self, sales_df: pd.DataFrame,
                                 calendar_df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform M5 wide format to long format time series.
        
        Args:
            sales_df: Sales data in wide format (columns are days)
            calendar_df: Calendar data mapping d_XXX to dates
            
        Returns:
            Long format DataFrame with date, store_id, item_id, units_sold
        """
        print("Transforming to long format...")
        
        # Extract metadata columns
        id_cols = ['id', 'item_id', 'dept_id', 'cat_id', 'store_id', 'state_id']
        
        # Get day columns (d_1, d_2, ...)
        day_cols = [col for col in sales_df.columns if col.startswith('d_')]
        
        # Melt to long format
        df_long = sales_df.melt(
            id_vars=id_cols,
            value_vars=day_cols,
            var_name='d',
            value_name='units_sold'
        )
        
        # Merge with calendar to get actual dates
        calendar_subset = calendar_df[['d', 'date', 'wday', 'month', 'year', 
                                       'event_name_1', 'event_type_1']].copy()
        df_long = df_long.merge(calendar_subset, on='d', how='left')
        
        # Convert date to datetime
        df_long['date'] = pd.to_datetime(df_long['date'])
        
        # Add event flag
        df_long['has_event'] = (~df_long['event_name_1'].isna()).astype(int)
        
        print(f"  Long format shape: {df_long.shape}")
        return df_long
    
    def aggregate_to_store_category(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aggregate from SKU level to store-category level.
        
        Args:
            df: Long format DataFrame with SKU-level data
            
        Returns:
            Aggregated DataFrame at store-category level
        """
        print("Aggregating to store-category level...")
        
        # Group by store, category, and date
        group_cols = ['store_id', 'cat_id', 'date']
        calendar_cols = ['wday', 'month', 'year', 'has_event']
        
        # Aggregate sales
        agg_dict = {'units_sold': 'sum'}
        
        # Keep calendar features (should be same for all items on a date)
        for col in calendar_cols:
            if col in df.columns:
                agg_dict[col] = 'first'
        
        df_agg = df.groupby(group_cols, as_index=False).agg(agg_dict)
        
        # Sort by store, category, date
        df_agg = df_agg.sort_values(['store_id', 'cat_id', 'date']).reset_index(drop=True)
        
        print(f"  Aggregated shape: {df_agg.shape}")
        print(f"  Unique store-category combinations: {df_agg.groupby(['store_id', 'cat_id']).ngroups}")
        
        return df_agg
    
    def add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add time-based features from date column.
        
        Args:
            df: DataFrame with date column
            
        Returns:
            DataFrame with additional time features
        """
        print("Adding time features...")
        df = df.copy()
        
        df['day_of_week'] = df['date'].dt.dayofweek
        df['week_of_year'] = df['date'].dt.isocalendar().week
        df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
        
        print(f"  Added time features: day_of_week, week_of_year, is_weekend")
        return df
