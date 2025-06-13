import pandas as pd
import forestplot as fp
import matplotlib.pyplot as plt


def create_forest_plot(data):
    """
    Create forest plot for given data with proper label positioning and sorting.
    
    This version works with the standard pip-installed forestplot package.
    All custom sorting and fixes are implemented within this script.
    """
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

    # Calculate figure size: taller and narrower for better readability
    height = max(20, len(data) * 0.4)  # 0.4 inches per row for adequate spacing
    figsize = (10, height)  # 10 inches wide for compact display
    
    # CUSTOM SORTING LOGIC (replaces package modifications)
    # This ensures baseline appears first, then 'vs ...' labels alphabetically
    def custom_sort_key(row):
        predictor = row['predictor']
        label = str(row['label']).strip().lower()
        time_period = row['time_period']
        
        # Get predictor order
        try:
            pred_order = selected_predictors.index(predictor)
        except ValueError:
            pred_order = 999
        
        # Get label order within predictor
        if label == 'baseline':
            label_order = 0
        elif label.startswith('vs '):
            label_order = 1
        else:
            label_order = 2
            
        return (pred_order, time_period, label_order, label)
    
    # Apply custom sorting
    data['sort_key'] = data.apply(custom_sort_key, axis=1)
    data = data.sort_values('sort_key').drop('sort_key', axis=1).reset_index(drop=True)
    
    # Preserve the order of predictors as specified
    predictor_order = [p for p in selected_predictors if p in data['predictor'].unique()]
    
    # Create forest plot
    ax = fp.mforestplot(
            dataframe=data,
            estimate="metric",
            ll="ci_lower", hl="ci_upper",
            varlabel="label",
            capitalize=False,
            model_col="time_period",
            modellabels=["Time A", "Time B", "Time C"],
            mcolor=["#CC6677", "#4477AA", "#77CC66"],
            groupvar="predictor",
            group_order=predictor_order,
            color_alt_rows=True,
            sort=False,  # Don't sort - we pre-sorted the data
            pval="p_value",
            xlabel="Odds Ratio (95% CI)",
            ylabel="Predictors",
            title="Odds Ratio Comparison to Patients at Time A with the Baseline Characteristic",
            figsize=figsize, 
            **{
                "markersize": 35,
                "offset": 0.35,  
                "fontsize": 12,
                "grouplab_size": 14,
                # Vertical reference line at OR = 1
                "xline": 1,
                "xlinestyle": (0, (10, 5)),
                "xlinecolor": "#808080",
                "xlinewidth": 1.5,
                "xlim": (0, 2.5),
            }
        )

    # CRITICAL FIX: Manual label positioning to ensure visibility
    # This fixes the forestplot package's positioning issues with large figures
    ax.tick_params(axis='y', which='major', pad=20)
    for label in ax.get_yticklabels():
        label.set_horizontalalignment('right')
        label.set_x(-0.02)  # Position labels close to plot area

    # Enable subplot configuration tool
    plt.subplots_adjust(left=0.4, right=0.9, top=0.95, bottom=0.05)

    return ax


# Main execution
if __name__ == "__main__":
    df_sorted = pd.read_csv('forest_plot_20250612.csv')
    ax = create_forest_plot(df_sorted)
    plt.show()
    plt.savefig('mt_results/summary_forest_plot.png', dpi=400, bbox_inches='tight') 