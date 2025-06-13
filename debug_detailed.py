import pandas as pd
import forestplot as fp
import matplotlib.pyplot as plt

# Load and prepare data exactly like mt_code.py
df = pd.read_csv('forest_plot_20250612.csv')
selected_predictors = [
    'age_group', 'sex', 'obesity', 'smokingstatus', 'diabetes', 
    'anxiety', 'depression', 'radiculopathy', 'sciatica', 
    'discpathology', 'spinalstenosis', 'raceethnicity'
]
data = df[df['predictor'].isin(selected_predictors)]

print(f"Total filtered data rows: {len(data)}")

# Apply same sorting as mt_code.py
def label_sort_key(label):
    label_stripped = str(label).strip().lower()
    if label_stripped == 'baseline':
        return (0, '')
    elif label_stripped.startswith('vs '):
        return (1, label_stripped)
    else:
        return (2, label_stripped)

data['label_order'] = data['label'].map(label_sort_key)
data = data.sort_values(['predictor', 'time_period', 'label_order'])

# Test 1: Small subset with normal settings
print("\n=== Test 1: Small subset ===")
small_data = data.head(30)
fig, ax = plt.subplots(figsize=(10, 8))
ax = fp.mforestplot(
    dataframe=small_data,
    estimate="metric",
    ll="ci_lower", hl="ci_upper",
    varlabel="label",
    model_col="time_period",
    groupvar="predictor",
    figsize=(10, 8),
    fontsize=12
)
print(f"Small subset - Y-tick labels visible: {len([l for l in ax.get_yticklabels() if l.get_text().strip()])}")
plt.subplots_adjust(left=0.6, right=0.95, top=0.96, bottom=0.04)
plt.savefig('debug_small_subset.png', dpi=200, bbox_inches='tight')
plt.close()

# Test 2: Full data with current mt_code.py settings
print("\n=== Test 2: Full data current settings ===")
height = max(16, min(len(data) * 0.25, 30))
figsize = (12, height)
print(f"Figure size: {figsize}")

fig, ax = plt.subplots(figsize=figsize)
ax = fp.mforestplot(
    dataframe=data,
    estimate="metric",
    ll="ci_lower", hl="ci_upper",
    varlabel="label",
    model_col="time_period",
    modellabels=["Time A", "Time B", "Time C"],
    mcolor=["#CC6677", "#4477AA", "#77CC66"],
    groupvar="predictor",
    sort=False,
    pval="p_value",
    figsize=figsize,
    fontsize=14,
    grouplab_size=16,
    markersize=40
)

print(f"Full data - Y-axis limits: {ax.get_ylim()}")
print(f"Full data - Number of y-tick labels: {len(ax.get_yticklabels())}")
print(f"Full data - Y-tick labels with text: {len([l for l in ax.get_yticklabels() if l.get_text().strip()])}")

# Check label positions before and after subplots_adjust
label_positions_before = [(i, label.get_text()[:50]) for i, label in enumerate(ax.get_yticklabels()) if label.get_text().strip()]
print(f"Labels before adjust (first 5): {label_positions_before[:5]}")

plt.subplots_adjust(left=0.6, right=0.95, top=0.96, bottom=0.04)

label_positions_after = [(i, label.get_text()[:50]) for i, label in enumerate(ax.get_yticklabels()) if label.get_text().strip()]
print(f"Labels after adjust (first 5): {label_positions_after[:5]}")

plt.savefig('debug_full_current.png', dpi=200, bbox_inches='tight')
plt.close()

print("\nDebug plots saved: debug_small_subset.png, debug_full_current.png") 