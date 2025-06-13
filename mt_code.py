import pandas as pd
import forestplot as fp
import matplotlib.pyplot as plt


# Function to create forest plot
def create_forest_plot(data):
    """Create forest plot for given data"""
    if len(data) == 0:
        print(f"No data available for forest plot")
        return None

    # Filter to include age_group, sex, and 10 additional clinically relevant variables
    selected_predictors = [
        'age_group', 'sex', 'obesity', 'smokingstatus', 'diabetes', 
        'anxiety', 'depression', 'radiculopathy', 'sciatica', 
        'discpathology', 'spinalstenosis', 'raceethnicity'
    ]
    data = data[data['predictor'].isin(selected_predictors)]

    # Calculate appropriate figure size based on number of rows
    # Account for forestplot package's automatic y-axis compression
    height = max(20, len(data) * 0.4)  # Increased from 0.3 to 0.4 inches per row, minimum 20 inches
    figsize = (14, height)  # Make it wider too for better readability
    
    # Preserve the order of predictors as specified in our selection
    predictor_order = [p for p in selected_predictors if p in data['predictor'].unique()]
    
    # For each predictor, order labels as: baseline first, then sorted 'vs ...' labels
    def label_sort_key(label):
        label_stripped = str(label).strip().lower()
        if label_stripped == 'baseline':
            return (0, '')
        elif label_stripped.startswith('vs '):
            return (1, label_stripped)
        else:
            return (2, label_stripped)  # fallback for any unexpected label

    # Sort by predictor, then time_period, then label order within each predictor-time combination
    data['label_order'] = data['label'].map(label_sort_key)
    data = data.sort_values(['predictor', 'time_period', 'label_order'])
    
    # Create forest plot using mforestplot
    ax = fp.mforestplot(
            dataframe=data,
            estimate="metric",              # odds ratio
            ll="ci_lower", hl="ci_upper",   # confidence intervals
            varlabel="label",        # variable label 
            capitalize=False,        # don't capitalize labels
            model_col="time_period",
            modellabels=["Time A", "Time B", "Time C"],  # Match order in data
            mcolor=["#CC6677", "#4477AA", "#77CC66"],   # Match colors to time periods
            groupvar="predictor",    # grouping variable
            group_order=predictor_order,  # Ensure group order is respected
            color_alt_rows=True,
            sort=False,              # don't sort since we pre-sorted the data
            pval="p_value",  # Column of p-value to be reported on right
            xlabel="Odds Ratio (95% CI)",    # x-axis label
            ylabel="Predictors",             # y-axis label
            title="Odds Ratio Comparison to Patients at Time A with the Baseline Characteristic",
            figsize=figsize, 
            **{
                "markersize": 30,
                "offset": 0.35,  
                # Vertical reference line parameters:
                "xline": 1,                    # Position of vertical reference line
                "xlinestyle": (0, (10, 5)),    # Line style (long dash)
                "xlinecolor": "#808080",       # Line color (gray)
                "xlinewidth": 1.5,             # Line width
                "xlim": (0, 2.5),              # (min, max) values * MUST BE NOTED IN THE CAPTION
            }
        )

    # Customize appearance and fix layout
    plt.subplots_adjust(left=0.4, right=0.85, top=0.95, bottom=0.05)  # Adjust margins
    return ax

df_sorted = pd.read_csv('forest_plot_20250612.csv')
ax = create_forest_plot(df_sorted)
plt.show()
plt.savefig('mt_results/summary_forest_plot.png', dpi=300, bbox_inches='tight')


