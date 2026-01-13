"""
Base model interface for all forecasting models.
"""
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class ForecastModel(ABC):
    """Abstract base class for all forecasting models."""
    
    def __init__(self, name: str):
        """
        Initialize the model.
        
        Args:
            name: Name of the model
        """
        self.name = name
        self.is_fitted = False
    
    @abstractmethod
    def fit(self, train_data: pd.DataFrame, target_col: str = 'units_sold'):
        """
        Fit the model on training data.
        
        Args:
            train_data: Training data
            target_col: Name of target column
        """
        pass
    
    @abstractmethod
    def predict(self, horizon: int, future_dates: pd.DatetimeIndex = None) -> np.ndarray:
        """
        Generate forecasts for the given horizon.
        
        Args:
            horizon: Number of periods to forecast
            future_dates: Optional future dates for prediction
            
        Returns:
            Array of predictions
        """
        pass
    
    def get_name(self) -> str:
        """Get model name."""
        return self.name
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
