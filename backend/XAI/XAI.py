import pandas as pd
import numpy as np
import json, joblib, pickle, time

from sklearn.preprocessing import OrdinalEncoder

from XAI_funnctions import aggregate_lime_explanations, plot_top_feature_importance, train_optimum_model


def XAI_output(file_name):
    df = pd.read_csv(file_name)

    X = df.iloc[:, 3:21]
    y = df['cluster']

    # Load the column order
    with open('column_order.json', 'r') as file:
        column_order = json.load(file)

    # Reorder columns to match the training data
    X = X[column_order]

    numerical_cols = ['Tot Fwd Pkts Category', 'Tot Bwd Pkts Category',
                      'Flow Duration Category', 'TotLen Fwd Pkts Category',
                      'TotLen Bwd Pkts Category', 'Flow IAT Mean Category',
                      'Pkt Size Avg Category', 'Fwd Act Data Pkts Category',
                      'Init Fwd Win Byts Category', 'Bwd Pkts/s Category',
                      'Fwd Pkts/s Category', 'Subflow Bwd Byts Category']
    categorical_cols = ['Dst Port',
                        'Protocol', 'Fwd Seg Size Min', 'SYN Flag Cnt', 'ACK Flag Cnt',
                        'PSH Flag Cnt']

    # Convert columns to 'object' data type (if they are categorical, ensure they are strings)
    X[categorical_cols] = X[categorical_cols].astype(str)

    # Convert columns to 'int64' data type
    # X[numerical_cols] = X[numerical_cols].astype('int64')

    # categorical_cols = X.select_dtypes(include=['object']).columns
    # numerical_cols = X.select_dtypes(include=['int64']).columns

    # Iterate over the columns and replace NaN values
    for idx, column in enumerate(numerical_cols):
        X[column] = X[column].fillna(-1)

    # Iterate over the columns and replace NaN values
    for idx, column in enumerate(categorical_cols):
        X[column] = X[column].fillna('NULL')

    # Encode categorical features
    encoder = OrdinalEncoder()
    X[categorical_cols] = encoder.fit_transform(X[categorical_cols])

    column_mapping = {
        'Tot Fwd Pkts Category': 'Total Forward Packets',
        'Tot Bwd Pkts Category': 'Total Backward Packets',
        'Flow Duration Category': 'Flow Duration',
        'TotLen Fwd Pkts Category': 'Total Length of Forward Packets',
        'TotLen Bwd Pkts Category': 'Total Length of Backward Packets',
        'Flow IAT Mean Category': 'Flow Inter-Arrival Time Mean',
        'Pkt Size Avg Category': 'Average Packet Size',
        'Fwd Act Data Pkts Category': 'Forward Active Data Packets',
        'Bwd Pkts/s Category': 'Backward Packets per Second',
        'Fwd Pkts/s Category': 'Forward Packets per Second',
        'Subflow Bwd Byts Category': 'Subflow Backward Bytes',
        'Dst Port': 'Destination Port',
        'Protocol': 'Protocol',
        'SYN Flag Cnt': 'SYN Flag Count',
        'ACK Flag Cnt': 'ACK Flag Count',
        'PSH Flag Cnt': 'PSH Flag Count',
        'Init Fwd Win Byts Category': 'Initial Forward Window Bytes',
        'Fwd Seg Size Min': 'Minimum Forward Segment Size'
    }
    x_mapped = X.rename(columns=column_mapping)
    # Create the categorical_names dictionary

    # Get the indices of the categorical columns
    categorical_indices = [X.columns.get_loc(col) for col in categorical_cols]

    # Create the categorical_names dictionary
    categorical_names = {categorical_indices[i]: list(encoder.categories_[i]) for i in range(len(categorical_cols))}

    # model_HGB = train_optimum_model(X, y)
    # Later, to load the model back
    with open('best_hgb_model.pkl', 'rb') as file:
        model_HGB = pickle.load(file)

    Explanation = []

    for label_to_explain in (list(sorted(set(y)))):
        # for label_to_explain in list(np.sort(set(y_all))):
        aggregated_importance = aggregate_lime_explanations(model_HGB, X, y, x_mapped.columns, categorical_cols,
                                                            categorical_names, label_to_explain)
        plot_top_feature_importance(aggregated_importance, label_to_explain)
        # Explanation.append([aggregated_importance, label_to_explain])

        # print(f"Explanation for {label_to_explain} Done")

    print(Explanation)


# Start time
start_time = time.time()

XAI_output("cluster_data.csv")

# Later, to load the model back
# End time
end_time = time.time()

# Calculate execution time
execution_time = (end_time - start_time)/60.0
print(f"Execution time: {execution_time} minutes")