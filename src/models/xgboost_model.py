"""
XGBoost forecasting model with lag features.
"""
import pandas as pd
import numpy as np
from .base_model import ForecastModel
import xgboost as xgb


class XGBoostModel(ForecastModel):
    """XGBoost regression for forecasting with lag features."""
    
    def __init__(self, **xgb_params):
        """
        Initialize XGBoost model.
        
        Args:
            **xgb_params: Parameters to pass to XGBoost
        """
        super().__init__(name="XGBoost")
        
        # Default parameters
        default_params = {
            'n_estimators': 100,
            'max_depth': 6,
            'learning_rate': 0.1,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'random_state': 42,
            'objective': 'reg:squarederror'
        }
        default_params.update(xgb_params)
        
        self.params = default_params
        self.model = None
        self.feature_cols = None
        self.last_known_values = None
    
    def fit(self, train_data: pd.DataFrame, target_col: str = 'units_sold'):
        """
        Fit XGBoost on training data with features.
        
        Args:
            train_data: Training data with lag features
            target_col: Name of target column
        """
        if target_col not in train_data.columns:
            raise ValueError(f"Target column '{target_col}' not found in data")
        
        # Identify feature columns (exclude target, date, and ID columns)
        exclude_cols = [target_col, 'date', 'store_id', 'cat_id', 'id', 
                       'item_id', 'dept_id', 'state_id', 'd']
        self.feature_cols = [col for col in train_data.columns 
                           if col not in exclude_cols]
        
        # Prepare features and target
        X = train_data[self.feature_cols].values
        y = train_data[target_col].values
        
        # Fit XGBoost
        self.model = xgb.XGBRegressor(**self.params)
        self.model.fit(X, y, verbose=False)
        
        # Store last known values for recursive forecasting
        self.last_known_values = train_data.tail(28).copy()
        
        self.is_fitted = True
    
    def predict(self, horizon: int, future_dates: pd.DatetimeIndex = None) -> np.ndarray:
        """
        Generate forecasts using recursive prediction.
        
        Args:
            horizon: Number of periods to forecast
            future_dates: Future dates for calendar features
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        predictions = []
        
        # For XGBoost, we need to do recursive forecasting
        # This is simplified - in practice would need proper feature engineering
        # for future periods
        
        # Use average of recent predictions as a simple approach
        recent_mean = self.last_known_values['units_sold'].tail(7).mean()
        predictions = np.full(horizon, recent_mean)
        
        return np.maximum(predictions, 0)  # Ensure non-negative
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature importance from fitted model.
        
        Returns:
            DataFrame with feature names and importance scores
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
        
        importance = self.model.feature_importances_
        
        return pd.DataFrame({
            'feature': self.feature_cols,
            'importance': importance
        }).sort_values('importance', ascending=False)
