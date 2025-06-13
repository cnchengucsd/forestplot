# Forest Plot Setup Instructions

## Quick Setup for Mac

Follow these steps to set up the modified forestplot package and run the forest plot code:

### Step 1: Clone the Modified Repository
```bash
# Clone the forked repository with modifications
git clone https://github.com/cnchengucsd/forestplot.git
cd forestplot

# Switch to the branch with modifications
git checkout test_mt
```

### Step 2: Set Up Python Environment
```bash
# Create a virtual environment (recommended)
python3 -m venv forestplot_env
source forestplot_env/bin/activate

# Install the modified forestplot package in development mode
pip install -e .

# Install additional dependencies
pip install pandas matplotlib
```

### Step 3: Prepare Your Data
- Place your CSV file in the `forestplot` directory
- Rename it to `forest_plot_20250612.csv`
- Ensure it has these columns:
  - `predictor`: grouping variable (e.g., 'age_group', 'sex', etc.)
  - `label`: row labels (e.g., 'baseline', 'vs category1', etc.)
  - `metric`: odds ratio values
  - `ci_lower`: lower confidence interval
  - `ci_upper`: upper confidence interval  
  - `p_value`: p-values
  - `time_period`: time categories for different colored markers

### Step 4: Create Output Directory
```bash
mkdir -p mt_results
```

### Step 5: Run the Forest Plot Code
```bash
python mt_code.py
```

### Step 6: View Results
- The plot will display on screen
- A high-resolution PNG will be saved to `mt_results/summary_forest_plot.png`

## Key Features of This Modified Version

✅ **Custom Label Sorting**: Baseline labels appear first, then "vs ..." labels alphabetically within each predictor group

✅ **Fixed Label Positioning**: Labels are properly positioned and visible (fixes original package issues)

✅ **Optimized Dimensions**: Taller and narrower plot for better readability

✅ **Interactive Subplot Tool**: Use matplotlib's configuration tool to adjust layout

## Verification

To verify you're using the modified version, run:
```bash
python -c "import forestplot; print('Location:', forestplot.__file__)"
```

You should see a path ending with your cloned `forestplot` directory, not a system-wide installation.

## Troubleshooting

### If you get import errors:
```bash
# Make sure you're in the forestplot directory and virtual environment is activated
source forestplot_env/bin/activate
pip install -e .
```

### If labels still appear in wrong order:
- Verify you're on the `test_mt` branch: `git branch`
- Verify the modifications are present in the package files

### If plot looks compressed:
- Use the matplotlib subplot configuration tool (appears when plot is displayed)
- Adjust the `left` margin to around 0.4-0.6 for optimal label visibility

## Files You Need

Send your colleague:
1. These setup instructions
2. Their CSV data file
3. (Optional) The `mt_code.py` file if you've made additional customizations

The modified forestplot package will be downloaded directly from your GitHub repository. 