import pandas as pd
import forestplot as fp
import matplotlib.pyplot as plt


def create_forest_plot(data):
    """
    Create forest plot for given data with proper label positioning and sorting.
    
    This version works with the modified forestplot package that has custom sorting.
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
    data = data[data['predictor'].isin(selected_predictors)].copy()

    # Calculate figure size: taller and narrower for better readability
    height = max(20, len(data) * 0.4)  # 0.4 inches per row for adequate spacing
    figsize = (10, height)  # 10 inches wide for compact display
    
    # Preserve the order of predictors as specified
    predictor_order = [p for p in selected_predictors if p in data['predictor'].unique()]
    
    # Create forest plot - the modified package handles custom sorting
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
            sort=True,  # Modified package handles custom sorting
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
        # Position labels within the plot area instead of outside
        label.set_x(0.05)  # Positive value to keep labels inside figure bounds

    # Enable subplot configuration tool and set proper margins
    plt.subplots_adjust(left=0.64, right=0.9, top=1, bottom=0.173)

    return ax


# Alternative saving approach - copy this into mt_code.py if the main version doesn't work

# Main execution
if __name__ == "__main__":
    df_sorted = pd.read_csv('forest_plot_20250612.csv')
    ax = create_forest_plot(df_sorted)
    
    # Get the figure and force it to draw
    fig = plt.gcf()
    fig.canvas.draw()  # Force drawing
    
    # Save with multiple approaches
    print("Saving forest plot...")
    
    # Method 1: Direct save
    fig.savefig('mt_results/summary_forest_plot_v1.png', dpi=400, 
                facecolor='white', edgecolor='none')
    
    # Method 2: With bbox_inches
    fig.savefig('mt_results/summary_forest_plot_v2.png', dpi=400, 
                bbox_inches='tight', facecolor='white')
    
    # Method 3: Using plt.savefig
    plt.savefig('mt_results/summary_forest_plot_v3.png', dpi=400, 
                facecolor='white', edgecolor='none')
    
    print("Multiple versions saved - check which one works!")
    
    # Show the plot
    plt.show() 