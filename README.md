# Forest Plot Generator

This script generates forest plots with proper label sorting and positioning.

## Two Versions Available

### 1. Standalone Version (Recommended for sharing)
- **File**: `mt_code_standalone.py`
- **Works with**: Standard pip-installed forestplot package
- **Best for**: Sharing with colleagues who don't want to modify packages

### 2. Enhanced Version (Current development version)
- **File**: `mt_code.py` 
- **Requires**: Modified forestplot package (custom repository)
- **Best for**: Development and advanced customization

## Quick Setup (Standalone Version)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the standalone script:**
   ```bash
   python mt_code_standalone.py
   ```

## Requirements

- Your CSV file should be named `forest_plot_20250612.csv` and placed in the same directory
- The script will create a `mt_results/` directory and save the plot as `summary_forest_plot.png`

## Key Features

- **Custom sorting**: Baseline labels appear first, then "vs ..." labels alphabetically within each predictor group
- **Fixed label positioning**: Labels are properly positioned and visible (fixes forestplot package issues)
- **Optimized dimensions**: Taller and narrower plot for better readability
- **Interactive**: Use matplotlib's subplot configuration tool to adjust layout
- **Standalone compatibility**: Works with standard forestplot package from PyPI

## Data Format

Your CSV should have these columns:
- `predictor`: grouping variable (e.g., 'age_group', 'sex', etc.)
- `label`: row labels (e.g., 'baseline', 'vs category1', etc.)
- `metric`: odds ratio values
- `ci_lower`: lower confidence interval
- `ci_upper`: upper confidence interval  
- `p_value`: p-values
- `time_period`: time categories for different colored markers

## For Your Colleague

Send them these files:
1. `mt_code_standalone.py` (the main script)
2. `requirements.txt` (dependencies)
3. `README.md` (this file)
4. Their CSV data file (renamed to `forest_plot_20250612.csv`)

They can then run `pip install -r requirements.txt` and `python mt_code_standalone.py` without any package modifications!
