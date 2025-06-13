import pandas as pd
import forestplot as fp
from forestplot.mplot_dataframe_utils import insert_group_model
from forestplot.dataframe_utils import sort_groups, reverse_dataframe
from forestplot.text_utils import normalize_varlabels, indent_nongroupvar, format_varlabels

def debug_step(df, step_name):
    print(f"\n=== {step_name} ===")
    print(f"Shape: {df.shape}")
    if 'label' in df.columns and 'predictor' in df.columns:
        print("Sample of label ordering:")
        for pred in ['age_group', 'sex', 'obesity'][:3]:  # Just show first 3 predictors
            pred_data = df[df['predictor'] == pred]
            if len(pred_data) > 0:
                print(f"  {pred}:")
                for _, row in pred_data.head(6).iterrows():  # Show first 6 rows per predictor
                    label = row.get('label', 'N/A')
                    time_period = row.get('time_period', 'N/A')
                    print(f"    {label} ({time_period})")
    print("-" * 50)

# Load and filter data exactly like mt_code.py
df = pd.read_csv('forest_plot_20250612.csv')
selected_predictors = [
    'age_group', 'sex', 'obesity', 'smokingstatus', 'diabetes', 
    'anxiety', 'depression', 'radiculopathy', 'sciatica', 
    'discpathology', 'spinalstenosis', 'raceethnicity'
]
data = df[df['predictor'].isin(selected_predictors)]

debug_step(data, "1. Initial filtered data")

# Apply user's sorting
predictor_order = [p for p in selected_predictors if p in data['predictor'].unique()]

def label_sort_key(label):
    label_stripped = str(label).strip().lower()
    if label_stripped == 'baseline':
        return (0, '')
    elif label_stripped.startswith('vs '):
        return (1, label_stripped)
    else:
        return (2, label_stripped)

# Sort by predictor, then time_period, then label order within each predictor-time combination
data['label_order'] = data['label'].map(label_sort_key)
data = data.sort_values(['predictor', 'time_period', 'label_order'])

debug_step(data, "2. After user's custom sorting")

# Now simulate the mforestplot preprocessing steps
print("\n" + "="*60)
print("SIMULATING MFORESTPLOT PREPROCESSING")
print("="*60)

# Step 1: sort_groups (if group_order is provided)
if predictor_order:
    data_step1 = sort_groups(data.copy(), groupvar='predictor', group_order=predictor_order)
    debug_step(data_step1, "3. After sort_groups")
else:
    data_step1 = data.copy()

# Step 2: insert_group_model
data_step2 = insert_group_model(
    dataframe=data_step1,
    groupvar='predictor',
    varlabel='label',
    model_col='time_period'
)
debug_step(data_step2, "4. After insert_group_model")

# Step 3: normalize_varlabels
data_step3 = normalize_varlabels(
    dataframe=data_step2,
    varlabel='label',
    capitalize=None
)
debug_step(data_step3, "5. After normalize_varlabels")

# Step 4: indent_nongroupvar
data_step4 = indent_nongroupvar(
    dataframe=data_step3,
    varlabel='label',
    groupvar='predictor'
)
debug_step(data_step4, "6. After indent_nongroupvar")

# Step 5: format_varlabels
data_step5 = format_varlabels(
    dataframe=data_step4,
    varlabel='label',
    form_ci_report=False,
    ci_report=False,
    groupvar='predictor'
)
debug_step(data_step5, "7. After format_varlabels")

# Step 6: reverse_dataframe (this is the final step)
data_final = reverse_dataframe(data_step5)
debug_step(data_final, "8. After reverse_dataframe (FINAL)")

print("\n" + "="*60)
print("SUMMARY: Check if the final order matches your expectations")
print("="*60) 