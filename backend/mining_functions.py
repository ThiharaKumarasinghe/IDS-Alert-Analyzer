import pandas as pd # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns   # type: ignore


# Find the maximum value in a column
def get_max_and_min(column_name, df):
    maximum_value = df[column_name].max()

    # Find the minimum value in a column
    minimum_value = df[column_name].min()

    # Print the maximum and minimum values
    print("Maximum Value:", maximum_value)
    print("Minimum Value:", minimum_value)


# Function to categorize values based on ranges
def categorize_value(value, ranges):
    # if pd.isnull(value):
    # return 'unknown'  # Treat NaN values as 'unknown'
    for category, (lower, upper) in ranges.items():
        if lower <= value <= upper:
            return category
    # return 'unknown'


def adaptive_bin_handling(column_name, df, bin_data):
    bin_ranges, bin_edges = pd.qcut(df[f'{column_name}'], 10, labels=None, retbins=True, precision=2, duplicates='drop')
    # print(bin_ranges.value_counts())

    ranges = {}
    for idx in range(len(bin_edges) - 1):
        ranges.update({(bin_edges[idx] + bin_edges[idx + 1]) / 2: (bin_edges[idx], bin_edges[idx + 1])})

    bin_data.append([f"{column_name} Category", ranges])

    # Apply categorization to column
    df[f'{column_name} Category'] = df[f'{column_name}'].apply(lambda x: categorize_value(x, ranges))
    # print(df[f'{column_name} Category'].value_counts())

    # plt.figure(figsize=(20, 8))
    # sns.histplot(data=df, x=df[f'{column_name} Category'], hue='Label', multiple='stack', discrete='True')
    # plt.show()

    # print("\n================================================================================\n")

    return f"{column_name} Category", bin_data


def return_unique_labels(alertID_List,df):
    # Filter DataFrame based on selected IDs
    selected_records = df.iloc[alertID_List]
    # Count unique values in a certain field (e.g., Field1) in the selected records
    unique_value_counts = selected_records['Label'].value_counts().to_dict()
    return unique_value_counts

# Define function to get field and value
def get_field_and_value(num,reverse_mapping):
    for field, mapping in reverse_mapping.items():
        if num in mapping:
            return field, mapping[num]
    return "Unknown", "Unknown"

def map_ranges_to_pattern_df(pattern_df, categorization_data):
    # Create a dictionary for quick lookup of ranges
    pattern_df_mapped = pattern_df.copy()

    for category_data in categorization_data:
        column = category_data[0]
        ranges_dict = category_data[1]

        # Map the values in the column to their corresponding ranges
        pattern_df_mapped[column] = pattern_df[column].map(ranges_dict)
    
    return pattern_df_mapped
