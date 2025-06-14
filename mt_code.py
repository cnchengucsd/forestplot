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

    # Calculate figure size: optimized for display window fitting
    height = max(8, len(data) * 0.18)  # Further reduced to 0.18 inches per row
    figsize = (14, height)  # Wider to compensate for shorter height
    
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
            title="",  # Remove title to eliminate top whitespace
            figsize=figsize, 
            **{
                "markersize": 20,  # Further reduced for compact layout
                "offset": 0.2,    # Tighter spacing between markers
                "fontsize": 9,    # Smaller font for compact display
                "grouplab_size": 10,  # Smaller group labels
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
    ax.tick_params(axis='y', which='major', pad=15)  # Reduced padding from 20 to 15
    for label in ax.get_yticklabels():
        label.set_horizontalalignment('right')
        # Position labels within the plot area instead of outside
        label.set_x(0.05)  # Positive value to keep labels inside figure bounds

    # Enable subplot configuration tool and set proper margins
    plt.subplots_adjust(left=0.45, right=0.95, top=0.98, bottom=0.12)  # Minimal top margin, more compact

    return ax


# Main execution
if __name__ == "__main__":
    df_sorted = pd.read_csv('forest_plot_20250612.csv')
    ax = create_forest_plot(df_sorted)
    
    # Get the figure and ensure all adjustments are applied
    fig = plt.gcf()
    
    # Force the figure to draw and apply all adjustments
    fig.canvas.draw()
    
    # Apply subplot adjustments again with optimized margins for saving
    plt.subplots_adjust(left=0.45, right=0.95, top=0.98, bottom=0.12)
    
    # Adjust legend position for compact layout
    legend = ax.get_legend()
    if legend:
        # Move legend closer to the plot for compact layout
        legend.set_bbox_to_anchor((0.5, -0.04))  # Adjusted for compact figure
        legend.set_loc('upper center')
    
    # Save with the correct proportions
    print("Saving forest plot...")
    fig.savefig('mt_results/summary_forest_plot.png', dpi=400, 
                facecolor='white', edgecolor='none',
                bbox_inches=None)  # Don't use bbox_inches to preserve our subplot adjustments
    print("Forest plot saved to mt_results/summary_forest_plot.png")
    
    # Show the plot after saving
    plt.show()


