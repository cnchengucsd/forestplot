data['label_order'] = data.groupby('predictor')['label'].transform(
    lambda labels: labels.map(lambda l: label_sort_key(l))
)

# Debug: Print the label_order column for each predictor
print("\nActual label_order values in dataframe:")
for pred in predictor_order:
    subset = data[data['predictor'] == pred][['label', 'label_order']].drop_duplicates()
    print(f"{pred}:")
    for _, row in subset.iterrows():
        print(f"  '{row['label']}': {row['label_order']}")

data = data.sort_values(['predictor', 'label_order', 'time_period'])

# Debug: Print final sorted order for each predictor
print("\nFinal sorted order:")
for pred in predictor_order:
    labels_sorted = data[data['predictor'] == pred]['label'].drop_duplicates().tolist()
    print(f"{pred}: {labels_sorted}") 