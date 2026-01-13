"""
Rolling backtesting framework for time series models.
"""
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from models.base_model import ForecastModel
from evaluation.metrics import ForecastMetrics


class RollingBacktest:
    """Performs rolling-origin backtesting."""
    
    def __init__(self, train_window: int, horizon: int, step_size: int):
        """
        Initialize backtesting framework.
        
        Args:
            train_window: Number of days to use for training
            horizon: Number of days to forecast
            step_size: Number of days to slide window forward
        """
        self.train_window = train_window
        self.horizon = horizon
        self.step_size = step_size
    
    def run(self, data: pd.DataFrame, 
            model: ForecastModel,
            group_cols: List[str],
            target_col: str = 'units_sold',
            n_folds: int = 4) -> Dict:
        """
        Run rolling backtesting for a single time series.
        
        Args:
            data: Time series data for one group
            model: Forecasting model instance
            group_cols: Columns defining the group
            target_col: Target column name
            n_folds: Number of backtest folds
            
        Returns:
            Dictionary with predictions and metrics
        """
        data = data.sort_values('date').reset_index(drop=True)
        
        all_predictions = []
        all_actuals = []
        fold_metrics = []
        
        total_periods = len(data)
        
        # Check if we have enough data
        min_required = self.train_window + self.horizon
        if total_periods < min_required:
            print(f"  Warning: Not enough data ({total_periods} < {min_required} required)")
            return {
                'predictions': np.array([]),
                'actuals': np.array([]),
                'metrics': {'MAE': np.nan, 'RMSE': np.nan, 'MAPE': np.nan},
                'n_folds': 0
            }
        
        # Calculate how many folds we can actually do
        available_for_folds = total_periods - self.train_window - self.horizon
        max_possible_folds = max(1, available_for_folds // self.step_size)
        actual_folds = min(n_folds, max_possible_folds)
        
        if actual_folds < n_folds:
            print(f"  Note: Reduced to {actual_folds} folds due to data limitations")
        
        for fold in range(actual_folds):
            # Calculate indices for this fold
            train_start = fold * self.step_size
            train_end = train_start + self.train_window
            test_start = train_end
            test_end = test_start + self.horizon
            
            if test_end > total_periods:
                break
            
            # Split data
            train_data = data.iloc[train_start:train_end]
            test_data = data.iloc[test_start:test_end]
            
            # Fit and predict
            try:
                if len(train_data) < 28:  # Need minimum data
                    print(f"  Warning: Fold {fold} has only {len(train_data)} training samples, skipping")
                    continue
                    
                model.fit(train_data, target_col)
                predictions = model.predict(self.horizon)
                actuals = test_data[target_col].values
                
                if len(predictions) != len(actuals):
                    print(f"  Warning: Fold {fold} prediction length mismatch")
                    continue
                
                # Calculate metrics for this fold
                metrics = ForecastMetrics.calculate_all(actuals, predictions)
                
                # Check for valid metrics
                if not np.isnan(metrics['MAE']):
                    fold_metrics.append(metrics)
                    all_predictions.extend(predictions)
                    all_actuals.extend(actuals)
                else:
                    print(f"  Warning: Fold {fold} produced NaN metrics")
                
            except Exception as e:
                print(f"  Error in fold {fold}: {str(e)}")
                continue
        
        # Aggregate metrics across folds
        if fold_metrics:
            avg_metrics = {
                'MAE': np.mean([m['MAE'] for m in fold_metrics]),
                'RMSE': np.mean([m['RMSE'] for m in fold_metrics]),
                'MAPE': np.mean([m['MAPE'] for m in fold_metrics]),
            }
        else:
            avg_metrics = {'MAE': np.nan, 'RMSE': np.nan, 'MAPE': np.nan}
        
        return {
            'predictions': np.array(all_predictions),
            'actuals': np.array(all_actuals),
            'metrics': avg_metrics,
            'n_folds': len(fold_metrics)
        }
    
    def run_multiple_series(self, data: pd.DataFrame,
                           model_class,
                           group_cols: List[str],
                           target_col: str = 'units_sold',
                           n_folds: int = 4,
                           max_series: int = None) -> pd.DataFrame:
        """
        Run backtesting across multiple time series.
        
        Args:
            data: Full dataset with multiple time series
            model_class: Model class to instantiate
            group_cols: Columns defining each time series
            target_col: Target column name
            n_folds: Number of backtest folds
            max_series: Maximum number of series to test (for speed)
            
        Returns:
            DataFrame with aggregated results
        """
        print(f"\nRunning backtest for {model_class.__name__}...")
        
        groups = data.groupby(group_cols)
        n_groups = groups.ngroups
        
        if max_series:
            n_groups = min(n_groups, max_series)
        
        all_metrics = []
        
        for i, (group_key, group_data) in enumerate(groups):
            if max_series and i >= max_series:
                break
            
            # Create fresh model instance for each series
            model = model_class()
            
            # Run backtest
            results = self.run(group_data, model, group_cols, target_col, n_folds)
            
            metrics_dict = results['metrics'].copy()
            metrics_dict['group'] = str(group_key)
            metrics_dict['n_folds'] = results['n_folds']
            
            all_metrics.append(metrics_dict)
            
            if (i + 1) % 5 == 0:
                print(f"  Completed {i+1}/{n_groups} series")
        
        results_df = pd.DataFrame(all_metrics)
        
        # Calculate overall averages
        print(f"\n{model_class.__name__} Results:")
        print(f"  Mean MAE: {results_df['MAE'].mean():.2f}")
        print(f"  Mean RMSE: {results_df['RMSE'].mean():.2f}")
        print(f"  Mean MAPE: {results_df['MAPE'].mean():.2f}%")
        
        return results_df
