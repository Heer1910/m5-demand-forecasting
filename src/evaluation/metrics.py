"""
Evaluation metrics for forecasting models.
"""
import numpy as np
import pandas as pd
from typing import Dict


class ForecastMetrics:
    """Calculate forecasting accuracy metrics."""
    
    @staticmethod
    def mae(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Error.
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            
        Returns:
            MAE score
        """
        return np.mean(np.abs(y_true - y_pred))
    
    @staticmethod
    def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Root Mean Squared Error.
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            
        Returns:
            RMSE score
        """
        return np.sqrt(np.mean((y_true - y_pred) ** 2))
    
    @staticmethod
    def mape(y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """
        Calculate Mean Absolute Percentage Error.
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            
        Returns:
            MAPE score (as percentage)
        """
        # Avoid division by zero
        mask = y_true != 0
        if not mask.any():
            return np.nan
        
        return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100
    
    @staticmethod
    def calculate_all(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
        """
        Calculate all metrics.
        
        Args:
            y_true: Actual values
            y_pred: Predicted values
            
        Returns:
            Dictionary with all metrics
        """
        return {
            'MAE': ForecastMetrics.mae(y_true, y_pred),
            'RMSE': ForecastMetrics.rmse(y_true, y_pred),
            'MAPE': ForecastMetrics.mape(y_true, y_pred)
        }


def aggregate_metrics(metrics_list: list) -> pd.DataFrame:
    """
    Aggregate metrics across multiple folds.
    
    Args:
        metrics_list: List of metric dictionaries
        
    Returns:
        DataFrame with mean and std metrics
    """
    df = pd.DataFrame(metrics_list)
    
    summary = pd.DataFrame({
        'Mean': df.mean(),
        'Std': df.std()
    })
    
    return summary
