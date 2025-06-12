import pandas as pd
import forestplot as fp
import matplotlib.pyplot as plt


# Function to create forest plot
def create_forest_plot(data):
    """Create forest plot for given data"""
    if len(data) == 0:
        print(f"No data available for forest plot")
        return None

    # Calculate appropriate figure size based on number of rows
    height = max(12, len(data) * 0.2 )  # At least 0.4 inches per row plus margin
    figsize = (12, height)
    
    # Create forest plot
    ax = fp.mforestplot(
            dataframe=data,
            estimate="metric",              # odds ratio
            ll="ci_lower", hl="ci_upper",   # confidence intervals
            varlabel="label",        # variable label 
            capitalize=False,        # don't capitalize labels
            model_col="time_period",
            modellabels=["Time C", "Time B", "Time A"],
            mcolor=["#77CC66", "#4477AA", "#CC6677"],
            groupvar="predictor",    # grouping variable
            color_alt_rows=True,
            sort=False,              # sort within groups
            #group_order=data['predictor'].unique().tolist(),
            pval="p_value",  # Column of p-value to be reported on right
            xlabel="Odds Ratio (95% CI)",    # x-axis label
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

    # Customize appearance
    plt.tight_layout()
    return ax

df_sorted = pd.read_csv('forest_plot_20250612.csv')
ax = create_forest_plot(df_sorted)
plt.show()
plt.savefig('results/summary_forest_plot.png', dpi=300, bbox_inches='tight')


