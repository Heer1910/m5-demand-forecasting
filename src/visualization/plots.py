"""
Visualization utilities for forecasting results.
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os


# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)


class ForecastVisualizer:
    """Create visualizations for forecasting results."""
    
    def __init__(self, output_dir: str = "plots"):
        """
        Initialize visualizer.
        
        Args:
            output_dir: Directory to save plots
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def plot_forecast(self, 
                     actual: np.ndarray,
                     predicted: np.ndarray,
                     dates: pd.DatetimeIndex = None,
                     model_name: str = "Model",
                     title: str = None,
                     save_path: str = None):
        """
        Plot actual vs predicted values.
        
        Args:
            actual: Actual values
            predicted: Predicted values
            dates: Optional datetime index
            model_name: Name of the model
            title: Plot title
            save_path: Path to save plot
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        if dates is None:
            x = np.arange(len(actual))
            xlabel = "Time Period"
        else:
            x = dates
            xlabel = "Date"
        
        ax.plot(x, actual, label='Actual', color='#2E86AB', linewidth=2, marker='o', markersize=4)
        ax.plot(x, predicted, label='Predicted', color='#A23B72', linewidth=2, marker='s', markersize=4, linestyle='--')
        
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel('Units Sold', fontsize=12)
        ax.set_title(title or f'{model_name} - Actual vs Predicted', fontsize=14, fontweight='bold')
        ax.legend(fontsize=11)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            print(f"  Saved plot to {save_path}")
        
        plt.close()
    
    def plot_model_comparison(self,
                             results_df: pd.DataFrame,
                             metric: str = 'MAE',
                             title: str = None,
                             save_path: str = None):
        """
        Create bar chart comparing models.
        
        Args:
            results_df: DataFrame with model results
            metric: Metric to compare
            title: Plot title
            save_path: Path to save plot
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        # Sort by metric value
        plot_data = results_df.sort_values(metric)
        
        # Custom color palette - vibrant gradient
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
        if len(plot_data) > len(colors):
            colors = sns.color_palette("viridis", len(plot_data))
        else:
            colors = colors[:len(plot_data)]
        
        # Create horizontal bars with gradient effect
        bars = ax.barh(plot_data['model'], plot_data[metric], 
                       color=colors, edgecolor='#2C3E50', linewidth=2.5, alpha=0.85)
        
        # Add value labels on bars
        for i, (bar, value) in enumerate(zip(bars, plot_data[metric].values)):
            width = bar.get_width()
            # Position label inside if bar is wide enough, outside otherwise
            if width > plot_data[metric].max() * 0.15:
                label_x = width - (width * 0.05)
                ha = 'right'
                color = 'white'
                weight = 'bold'
            else:
                label_x = width + (plot_data[metric].max() * 0.02)
                ha = 'left'
                color = '#2C3E50'
                weight = 'normal'
            
            ax.text(label_x, bar.get_y() + bar.get_height()/2,
                   f'{value:.2f}',
                   ha=ha, va='center', fontsize=11, fontweight=weight, color=color)
        
        # Styling
        ax.set_xlabel(metric, fontsize=14, fontweight='bold', color='#2C3E50')
        ax.set_ylabel('Model', fontsize=14, fontweight='bold', color='#2C3E50')
        ax.set_title(title or f'Model Comparison - {metric} (Lower is Better)', 
                    fontsize=16, fontweight='bold', color='#2C3E50', pad=20)
        ax.grid(True, axis='x', alpha=0.3, linestyle='--', linewidth=0.8)
        ax.set_axisbelow(True)
        
        # Style spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#95A5A6')
        ax.spines['bottom'].set_color('#95A5A6')
        
        # Add winner annotation
        best_idx = 0  # First row after sorting (smallest value)
        best_value = plot_data.iloc[best_idx][metric]
        best_y_pos = best_idx
        
        ax.annotate('🏆 Best', 
                   xy=(best_value, best_y_pos),
                   xytext=(15, 0), textcoords='offset points',
                   fontsize=11, fontweight='bold', color='#27AE60',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#E8F8F5', 
                            edgecolor='#27AE60', linewidth=2),
                   va='center')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
            print(f"  Saved plot to {save_path}")
        
        plt.close()
    
    def plot_error_distribution(self,
                               errors: np.ndarray,
                               model_name: str = "Model",
                               save_path: str = None):
        """
        Plot distribution of forecast errors.
        
        Args:
            errors: Forecast errors (actual - predicted)
            model_name: Name of model
            save_path: Path to save plot
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
        
        # Histogram
        ax1.hist(errors, bins=50, color='#2E86AB', edgecolor='black', alpha=0.7)
        ax1.axvline(0, color='red', linestyle='--', linewidth=2, label='Zero Error')
        ax1.set_xlabel('Error (Actual - Predicted)', fontsize=12)
        ax1.set_ylabel('Frequency', fontsize=12)
        ax1.set_title(f'{model_name} - Error Distribution', fontsize=13, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Box plot
        ax2.boxplot(errors, vert=True, patch_artist=True,
                   boxprops=dict(facecolor='#A23B72', alpha=0.7),
                   medianprops=dict(color='red', linewidth=2))
        ax2.set_ylabel('Error', fontsize=12)
        ax2.set_title(f'{model_name} - Error Box Plot', fontsize=13, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=100, bbox_inches='tight')
            print(f"  Saved plot to {save_path}")
        
        plt.close()
    
    def create_results_table(self,
                            results_df: pd.DataFrame,
                            save_path: str = None) -> str:
        """
        Create formatted results table.
        
        Args:
            results_df: DataFrame with results
            save_path: Optional path to save as CSV
            
        Returns:
            Markdown formatted table string
        """
        if save_path:
            results_df.to_csv(save_path, index=False)
            print(f"  Saved results to {save_path}")
        
        # Create markdown table
        md_table = results_df.to_markdown(index=False, floatfmt=".2f")
        return md_table
