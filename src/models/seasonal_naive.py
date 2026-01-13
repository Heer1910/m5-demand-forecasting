"""
Seasonal Naive forecasting model - uses same day-of-week from previous period.
"""
import pandas as pd
import numpy as np
from .base_model import ForecastModel


class SeasonalNaiveModel(ForecastModel):
    """Seasonal Naive forecast - uses weekly seasonality."""
    
    def __init__(self, seasonal_period: int = 7):
        """
        Initialize seasonal naive model.
        
        Args:
            seasonal_period: Number of periods in season (default 7 for weekly)
        """
        super().__init__(name="Seasonal_Naive")
        self.seasonal_period = seasonal_period
        self.recent_values = None
    
    def fit(self, train_data: pd.DataFrame, target_col: str = 'units_sold'):
        """
        Fit by storing last seasonal_period values.
        
        Args:
            train_data: Training data
            target_col: Name of target column
        """
        if target_col not in train_data.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
        
        # Store last seasonal_period values
        self.recent_values = train_data[target_col].tail(self.seasonal_period).values
        self.is_fitted = True
    
    def predict(self, horizon: int, future_dates: pd.DatetimeIndex = None) -> np.ndarray:
        """
        Predict using seasonal pattern.
        
        Args:
            horizon: Number of periods to forecast
            future_dates: Not used for seasonal naive
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Repeat the seasonal pattern
        n_full_cycles = horizon // self.seasonal_period
        remainder = horizon % self.seasonal_period
        
        predictions = np.tile(self.recent_values, n_full_cycles + 1)[:horizon]
        
        return predictions
