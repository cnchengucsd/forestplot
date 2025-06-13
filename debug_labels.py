import pandas as pd
import forestplot as fp
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv('forest_plot_20250612.csv')
print(f"Total data rows: {len(df)}")

# Filter to a manageable subset for debugging
selected_predictors = ['age_group', 'sex', 'obesity']
df_subset = df[df['predictor'].isin(selected_predictors)]
print(f"Subset rows: {len(df_subset)}")

# Test with normal size first
print("\n=== Testing normal size ===")
fig, ax = plt.subplots(figsize=(10, 8))
ax = fp.mforestplot(
    dataframe=df_subset,
    estimate="metric",
    ll="ci_lower", hl="ci_upper",
    varlabel="label",
    model_col="time_period",
    groupvar="predictor",
    figsize=(10, 8),
    fontsize=12
)
print(f"Y-axis limits: {ax.get_ylim()}")
print(f"Y-tick labels: {[label.get_text() for label in ax.get_yticklabels()]}")
plt.savefig('debug_normal.png', dpi=150, bbox_inches='tight')
plt.close()

# Test with large size
print("\n=== Testing large size ===")
large_height = len(df_subset) * 0.4 + 10
fig, ax = plt.subplots(figsize=(14, large_height))
ax = fp.mforestplot(
    dataframe=df_subset,
    estimate="metric",
    ll="ci_lower", hl="ci_upper",
    varlabel="label",
    model_col="time_period",
    groupvar="predictor",
    figsize=(14, large_height),
    fontsize=14,
    grouplab_size=16
)
print(f"Y-axis limits: {ax.get_ylim()}")
print(f"Y-tick labels: {[label.get_text() for label in ax.get_yticklabels()]}")
print(f"Figure size: {fig.get_size_inches()}")
plt.savefig('debug_large.png', dpi=150, bbox_inches='tight')
plt.close()

print("Debug plots saved as debug_normal.png and debug_large.png") 