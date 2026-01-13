"""
Main pipeline for M5 demand forecasting project.
End-to-end workflow orchestration.
"""
import os
import sys
import yaml
import pandas as pd
import numpy as np
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from data.loader import M5DataLoader
from data.cleaner import DataCleaner
from data.transformer import DataTransformer
from features.lag_features import LagFeatureEngineer
from models.naive import NaiveModel
from models.seasonal_naive import SeasonalNaiveModel
from models.moving_average import MovingAverageModel
from models.arima import ARIMAModel
from models.xgboost_model import XGBoostModel
from evaluation.backtest import RollingBacktest
from evaluation.metrics import ForecastMetrics
from visualization.plots import ForecastVisualizer


class M5ForecastPipeline:
    """End-to-end forecasting pipeline."""
    
    def __init__(self, config_path: str = "src/config/config.yaml"):
        """
        Initialize pipeline with configuration.
        
        Args:
            config_path: Path to configuration file
        """
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.data = None
        self.processed_data = None
        self.results = {}
    
    def load_data(self, data_dir: str = None):
        """Load M5 dataset."""
        print("\n" + "="*60)
        print("STEP 1: LOADING DATA")
        print("="*60)
        
        if data_dir is None:
            data_dir = self.config['data']['raw_dir']
        
        loader = M5DataLoader(data_dir)
        sales_df, calendar_df, prices_df = loader.load_all()
        
        self.data = {
            'sales': sales_df,
            'calendar': calendar_df,
            'prices': prices_df
        }
        
        return self.data
    
    def process_data(self):
        """Process and transform data."""
        print("\n" + "="*60)
        print("STEP 2: PROCESSING DATA")
        print("="*60)
        
        # Transform to long format
        transformer = DataTransformer()
        df_long = transformer.transform_to_long_format(
            self.data['sales'],
            self.data['calendar']
        )
        
        # Aggregate to store-category level
        df_agg = transformer.aggregate_to_store_category(df_long)
        
        # Clean data
        cleaner = DataCleaner()
        df_clean = cleaner.clean(df_agg)
        df_clean = cleaner.remove_leading_zeros(
            df_clean,
            group_cols=['store_id', 'cat_id']
        )
        
        # Add time features
        df_clean = transformer.add_time_features(df_clean)
        
        # Save processed data
        output_path = os.path.join(self.config['data']['processed_dir'], 'processed_data.csv')
        os.makedirs(self.config['data']['processed_dir'], exist_ok=True)
        df_clean.to_csv(output_path, index=False)
        print(f"\n✓ Saved processed data to {output_path}")
        
        self.processed_data = df_clean
        return df_clean
    
    def create_features(self):
        """Create lag features for ML models."""
        print("\n" + "="*60)
        print("STEP 3: FEATURE ENGINEERING")
        print("="*60)
        
        engineer = LagFeatureEngineer(
            lag_days=self.config['features']['lag_days'],
            rolling_windows=self.config['features']['rolling_windows']
        )
        
        df_features = engineer.create_features(
            self.processed_data,
            group_cols=['store_id', 'cat_id']
        )
        
        # Remove incomplete rows
        df_features = engineer.remove_incomplete_rows(df_features)
        
        # Save featured data
        output_path = os.path.join(self.config['data']['processed_dir'], 'featured_data.csv')
        df_features.to_csv(output_path, index=False)
        print(f"\n✓ Saved featured data to {output_path}")
        
        self.featured_data = df_features
        return df_features
    
    def run_backtests(self, max_series: int = 10):
        """Run backtesting for all models."""
        print("\n" + "="*60)
        print("STEP 4: RUNNING BACKTESTS")
        print("="*60)
        
        # Initialize backtest framework
        backtest = RollingBacktest(
            train_window=self.config['backtest']['train_window'],
            horizon=self.config['forecast']['horizon'],
            step_size=self.config['backtest']['step_size']
        )
        
        # Models to test (baseline models on processed data)
        baseline_models = [
            NaiveModel,
            SeasonalNaiveModel,
            MovingAverageModel,
        ]
        
        # Store results
        all_results = []
        
        # Test baseline models
        print("\nTesting Baseline Models...")
        for model_class in baseline_models:
            try:
                results_df = backtest.run_multiple_series(
                    self.processed_data,
                    model_class,
                    group_cols=['store_id', 'cat_id'],
                    n_folds=self.config['backtest']['n_folds'],
                    max_series=max_series
                )
                
                if len(results_df) > 0 and not results_df['MAE'].isna().all():
                    # Aggregate metrics
                    avg_metrics = {
                        'model': model_class.__name__,
                        'MAE': results_df['MAE'].mean(),
                        'RMSE': results_df['RMSE'].mean(),
                        'MAPE': results_df['MAPE'].mean()
                    }
                    all_results.append(avg_metrics)
                else:
                    print(f"  ⚠️  {model_class.__name__} produced no valid results")
            except Exception as e:
                print(f"  ✗ {model_class.__name__} failed: {str(e)}")
                continue
        
        # Test ARIMA (computational expensive, limit to fewer series)
        print("\nTesting ARIMA Model...")
        try:
            results_df = backtest.run_multiple_series(
                self.processed_data,
                ARIMAModel,
                group_cols=['store_id', 'cat_id'],
                n_folds=min(2, self.config['backtest']['n_folds']),
                max_series=min(5, max_series)
            )
            avg_metrics = {
                'model': 'ARIMAModel',
                'MAE': results_df['MAE'].mean(),
                'RMSE': results_df['RMSE'].mean(),
                'MAPE': results_df['MAPE'].mean()
            }
            all_results.append(avg_metrics)
        except Exception as e:
            print(f"  ARIMA failed: {str(e)}")
        
        # Test XGBoost on featured data
        print("\nTesting XGBoost Model...")
        try:
            xgb_params = self.config['models']['xgboost']
            
            class ConfiguredXGBoost(XGBoostModel):
                def __init__(self):
                    super().__init__(**xgb_params)
            
            results_df = backtest.run_multiple_series(
                self.featured_data,
                ConfiguredXGBoost,
                group_cols=['store_id', 'cat_id'],
                n_folds=self.config['backtest']['n_folds'],
                max_series=max_series
            )
            avg_metrics = {
                'model': 'XGBoostModel',
                'MAE': results_df['MAE'].mean(),
                'RMSE': results_df['RMSE'].mean(),
                'MAPE': results_df['MAPE'].mean()
            }
            all_results.append(avg_metrics)
        except Exception as e:
            print(f"  XGBoost failed: {str(e)}")
        
        # Create results DataFrame
        self.results = pd.DataFrame(all_results)
        
        print("\n" + "="*60)
        print("BACKTEST RESULTS SUMMARY")
        print("="*60)
        print(self.results.to_string(index=False, float_format=lambda x: f'{x:.2f}'))
        
        return self.results
    
    def create_visualizations(self):
        """Create visualization plots."""
        print("\n" + "="*60)
        print("STEP 5: CREATING VISUALIZATIONS")
        print("="*60)
        
        if len(self.results) == 0:
            print("  ⚠️  No results to visualize")
            return
        
        viz = ForecastVisualizer(self.config['visualization']['output_dir'])
        
        # Model comparison charts
        for metric in ['MAE', 'RMSE', 'MAPE']:
            if metric in self.results.columns and not self.results[metric].isna().all():
                viz.plot_model_comparison(
                    self.results,
                    metric=metric,
                    save_path=os.path.join(self.config['visualization']['output_dir'], 
                                          f'model_comparison_{metric.lower()}.png')
                )
        
        # Save results table
        viz.create_results_table(
            self.results,
            save_path=os.path.join(self.config['visualization']['output_dir'],
                                  'results_summary.csv')
        )
        
        print("\n✓ All visualizations created")
    
    def run_full_pipeline(self, data_dir: str = None, max_series: int = 10):
        """Run the complete pipeline."""
        print("\n" + "="*60)
        print("M5 DEMAND FORECASTING PIPELINE")
        print("="*60)
        
        # Execute all steps
        self.load_data(data_dir)
        self.process_data()
        self.create_features()
        self.run_backtests(max_series=max_series)
        self.create_visualizations()
        
        # Identify best model
        if len(self.results) == 0 or self.results['MAE'].isna().all():
            print("\n" + "="*60)
            print("⚠️  WARNING: No models completed successfully")
            print("="*60)
            return
        
        # Filter out NaN results
        valid_results = self.results.dropna(subset=['MAE'])
        if len(valid_results) == 0:
            print("\n" + "="*60)
            print("⚠️  WARNING: No valid model results")
            print("="*60)
            return
            
        best_model = valid_results.loc[valid_results['MAE'].idxmin()]
        
        print("\n" + "="*60)
        print("PIPELINE COMPLETE")
        print("="*60)
        print(f"\n🏆 Best Model: {best_model['model']}")
        print(f"   MAE:  {best_model['MAE']:.2f}")
        print(f"   RMSE: {best_model['RMSE']:.2f}")
        print(f"   MAPE: {best_model['MAPE']:.2f}%")
        print("\n")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='M5 Demand Forecasting Pipeline')
    parser.add_argument('--data-dir', type=str, default='data/raw',
                       help='Directory containing M5 CSV files')
    parser.add_argument('--max-series', type=int, default=10,
                       help='Maximum number of time series to process')
    parser.add_argument('--config', type=str, default='src/config/config.yaml',
                       help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Run pipeline
    pipeline = M5ForecastPipeline(config_path=args.config)
    pipeline.run_full_pipeline(data_dir=args.data_dir, max_series=args.max_series)


if __name__ == '__main__':
    main()
