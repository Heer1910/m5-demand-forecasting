"""
Moving Average forecasting model.
"""
import pandas as pd
import numpy as np
from .base_model import ForecastModel


class MovingAverageModel(ForecastModel):
    """Moving average forecast."""
    
    def __init__(self, window: int = 7):
        """
        Initialize moving average model.
        
        Args:
            window: Size of moving average window
        """
        super().__init__(name=f"MA_{window}")
        self.window = window
        self.ma_value = None
    
    def fit(self, train_data: pd.DataFrame, target_col: str = 'units_sold'):
        """
        Fit by computing average of last window values.
        
        Args:
            train_data: Training data
            target_col: Name of target column
        """
        if target_col not in train_data.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
        
        # Compute moving average of last window values
        recent_values = train_data[target_col].tail(self.window).values
        self.ma_value = np.mean(recent_values)
        self.is_fitted = True
    
    def predict(self, horizon: int, future_dates: pd.DatetimeIndex = None) -> np.ndarray:
        """
        Predict by repeating the moving average value.
        
        Args:
            horizon: Number of periods to forecast
            future_dates: Not used for moving average
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Return MA value repeated for horizon
        return np.full(horizon, self.ma_value)
