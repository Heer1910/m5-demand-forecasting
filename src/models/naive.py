"""
Naive forecasting model - uses last observed value.
"""
import pandas as pd
import numpy as np
from .base_model import ForecastModel


class NaiveModel(ForecastModel):
    """Naive forecast - predicts last observed value."""
    
    def __init__(self):
        super().__init__(name="Naive")
        self.last_value = None
    
    def fit(self, train_data: pd.DataFrame, target_col: str = 'units_sold'):
        """
        Fit by storing the last observed value.
        
        Args:
            train_data: Training data
            target_col: Name of target column
        """
        if target_col not in train_data.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
        
        # Store last observed value
        self.last_value = train_data[target_col].iloc[-1]
        self.is_fitted = True
    
    def predict(self, horizon: int, future_dates: pd.DatetimeIndex = None) -> np.ndarray:
        """
        Predict by repeating the last observed value.
        
        Args:
            horizon: Number of periods to forecast
            future_dates: Not used for naive model
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Return last value repeated for horizon
        return np.full(horizon, self.last_value)
