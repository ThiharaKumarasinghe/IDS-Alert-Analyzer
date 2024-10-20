from collections import defaultdict
import json
import joblib, warnings  # type: ignore
import lime.lime_tabular  # type: ignore
from matplotlib import pyplot as plt  # type: ignore
import numpy as np
import pickle
import pandas as pd

from sklearn.preprocessing import OrdinalEncoder
from sklearn.ensemble import HistGradientBoostingClassifier  # type: ignore
from sklearn.model_selection import GridSearchCV  # type: ignore
from sklearn.pipeline import make_pipeline  # type: ignore
from sklearn.model_selection import train_test_split  # type: ignore
from sklearn.metrics import accuracy_score, classification_report  # type: ignore


def aggregate_lime_explanations(file_name,label_to_explain):

    """
    Aggregates LIME explanations for a certain class.

    Parameters:
    - model: Trained classifier.
    - X: Feature set.
    - y: Labels.
    - label_to_explain: The class to explain.
    - num_samples: Number of samples from the class to explain.

    Returns:
    - Aggregated feature importance for the class.
    """

    df = pd.read_csv(file_name)

    X = df.iloc[:, 2:21]
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
    with open('./XAI/best_hgb_model.pkl', 'rb') as file:
        model_HGB = pickle.load(file)


    # Suppress all FutureWarning messages
    warnings.simplefilter(action='ignore', category=FutureWarning)
    categorical_positions = [X.columns.get_loc(col) for col in categorical_cols]

    explainer = lime.lime_tabular.LimeTabularExplainer(
        X.values, mode='classification', feature_names=x_mapped.columns, class_names=list(sorted(set(y))),
        discretize_continuous=True, categorical_features=categorical_positions, categorical_names=categorical_names)

    label_indices = np.where(y == label_to_explain)[0]
    aggregated_importance = defaultdict(float)

    # Limit to num_samples or available instances for the selected label
    for i in range(len(label_indices)):
        instance_index = label_indices[i]
        test_instance = X.iloc[instance_index]

        # Generate LIME explanation for this instance
        exp = explainer.explain_instance(test_instance, model_HGB.predict_proba)

        # Aggregate feature importances
        for feature, importance in exp.as_list():
            aggregated_importance[feature] += importance

    # Normalize by the number of samples
    for feature in aggregated_importance:
        aggregated_importance[feature] /= len(label_indices)

    return dict(aggregated_importance)


# def plot_top_feature_importance(aggregated_importance, top_n, cluster_name):
#     # Sort features by importance in descending order
#     sorted_importance = sorted(aggregated_importance.items(), key=lambda x: x[1], reverse=True)
#
#     # Select the top N features (in this case, top 10)
#     top_features = sorted_importance[:top_n]
#
#     # Separate features and importance values
#     features, importance = zip(*top_features)
#
#     # Create a horizontal bar plot
#     plt.figure(figsize=(10, 6))
#     plt.barh(features, importance, color='skyblue')
#
#     # Add labels and title
#     plt.xlabel('Feature Importance')
#     plt.title(f'Top {top_n} Aggregated Feature Importance for Cluster {cluster_name}')
#
#     # Invert the y-axis to have the highest values at the top
#     plt.gca().invert_yaxis()
#
#     # Ensure layout fits nicely
#     plt.tight_layout()
#
#     # Display the plot
#     plt.show()


def plot_top_feature_importance(aggregated_importance, cluster_name):
    # Sort features by importance in descending order
    sorted_importance = sorted(aggregated_importance.items(), key=lambda x: x[1], reverse=True)

    # Select the top N features (in this case, top 10)
    top_features = sorted_importance[:len(sorted_importance)]

    # Separate features and importance values
    features, importance = zip(*top_features)

    # Create a horizontal bar plot
    plt.figure(figsize=(10, 6))
    plt.barh(features, importance, color='skyblue')

    # Add labels and title
    plt.xlabel('Feature Importance')
    plt.title(f'Aggregated Feature Importance for Cluster {cluster_name}')

    # Invert the y-axis to have the highest values at the top
    plt.gca().invert_yaxis()

    # Ensure layout fits nicely
    plt.tight_layout()

    # Display the plot
    plt.show()


def train_optimum_model(file_name):

    df = pd.read_csv(file_name)

    X = df.iloc[:, 2:21]
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

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # parameters to tune

    hgb_pipe = make_pipeline(HistGradientBoostingClassifier())

    # parameters = {
    #     'histgradientboostingclassifier__max_iter': [1000, 1200, 1500],
    #     'histgradientboostingclassifier__learning_rate': [0.1],
    #     'histgradientboostingclassifier__max_depth': [25, 50, 75],
    #     'histgradientboostingclassifier__l2_regularization': [1.5],
    #     'histgradientboostingclassifier__scoring': ['f1_micro'],
    #     'histgradientboostingclassifier__random_state': [42],
    # }
    parameters = {
        'histgradientboostingclassifier__max_iter': [1000],
        'histgradientboostingclassifier__learning_rate': [0.1],
        'histgradientboostingclassifier__max_depth': [25],
        'histgradientboostingclassifier__l2_regularization': [1.5],
        'histgradientboostingclassifier__scoring': ['f1_micro'],
        'histgradientboostingclassifier__random_state': [42],
    }

    # instantiate the gridsearch
    hgb_grid = GridSearchCV(hgb_pipe, parameters, n_jobs=5, cv=5, scoring='f1_macro', verbose=2, refit=True)
    # fit on the grid
    hgb_grid.fit(X_train.values, y_train.values)

    model_HGB = hgb_grid.best_estimator_

    
    # model_HGB.score(X_test.values, y_test.values)
    # print(accuracy)

    y_all = model_HGB.predict(X.values)
    full_report = classification_report(y.values, y_all)
    accuracy = accuracy_score(y.values, y_all)

    print(full_report)

    # Save the best estimator to a file
    with open('./XAI/best_hgb_model.pkl', 'wb') as file:
        pickle.dump(model_HGB, file)

    # return model_HGB
    return accuracy