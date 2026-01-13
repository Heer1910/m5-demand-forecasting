"""
ARIMA forecasting model using statsmodels.
"""
import pandas as pd
import numpy as np
from .base_model import ForecastModel
from statsmodels.tsa.statespace.sarimax import SARIMAX
import warnings


class ARIMAModel(ForecastModel):
    """ARIMA forecast using auto parameter selection."""
    
    def __init__(self, order: tuple = (1, 1, 1), 
                 seasonal_order: tuple = (1, 0, 1, 7)):
        """
        Initialize ARIMA model.
        
        Args:
            order: (p, d, q) order for ARIMA
            seasonal_order: (P, D, Q, s) seasonal order
        """
        super().__init__(name="ARIMA")
        self.order = order
        self.seasonal_order = seasonal_order
        self.model = None
        self.fitted_model = None
    
    def fit(self, train_data: pd.DataFrame, target_col: str = 'units_sold'):
        """
        Fit ARIMA model on training data.
        
        Args:
            train_data: Training data
            target_col: Name of target column
        """
        if target_col not in train_data.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
        
        # Extract time series
        y = train_data[target_col].values
        
        # Fit SARIMAX model
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            try:
                self.model = SARIMAX(
                    y,
                    order=self.order,
                    seasonal_order=self.seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )
                self.fitted_model = self.model.fit(disp=False, maxiter=100)
                self.is_fitted = True
            except Exception as e:
                # Fall back to simpler model if fit fails
                print(f"  Warning: ARIMA fit failed, falling back to (1,0,0): {str(e)}")
                self.model = SARIMAX(
                    y,
                    order=(1, 0, 0),
                    enforce_stationarity=False
                )
                self.fitted_model = self.model.fit(disp=False, maxiter=50)
                self.is_fitted = True
    
    def predict(self, horizon: int, future_dates: pd.DatetimeIndex = None) -> np.ndarray:
        """
        Generate ARIMA forecasts.
        
        Args:
            horizon: Number of periods to forecast
            future_dates: Not used for ARIMA
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        # Generate forecasts
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            forecasts = self.fitted_model.forecast(steps=horizon)
        
        # Ensure non-negative predictions
        forecasts = np.maximum(forecasts, 0)
        
        return forecasts
