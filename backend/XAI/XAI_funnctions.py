from collections import defaultdict
import joblib, warnings
import lime.lime_tabular
from matplotlib import pyplot as plt
import numpy as np
import pickle

from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report


def aggregate_lime_explanations(model, X, y, feature_names, categorical_columns, categorical_names, label_to_explain):
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

    # Suppress all FutureWarning messages
    warnings.simplefilter(action='ignore', category=FutureWarning)
    categorical_positions = [X.columns.get_loc(col) for col in categorical_columns]

    explainer = lime.lime_tabular.LimeTabularExplainer(
        X.values, mode='classification', feature_names=feature_names, class_names=list(sorted(set(y))),
        discretize_continuous=True, categorical_features=categorical_positions, categorical_names=categorical_names)

    label_indices = np.where(y == label_to_explain)[0]
    aggregated_importance = defaultdict(float)

    # Limit to num_samples or available instances for the selected label
    for i in range(len(label_indices)):
        instance_index = label_indices[i]
        test_instance = X.iloc[instance_index]

        # Generate LIME explanation for this instance
        exp = explainer.explain_instance(test_instance, model.predict_proba)

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


def train_optimum_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # parameters to tune

    hgb_pipe = make_pipeline(HistGradientBoostingClassifier())

    parameters = {
        'histgradientboostingclassifier__max_iter': [1000, 1200, 1500],
        'histgradientboostingclassifier__learning_rate': [0.1],
        'histgradientboostingclassifier__max_depth': [25, 50, 75],
        'histgradientboostingclassifier__l2_regularization': [1.5],
        'histgradientboostingclassifier__scoring': ['f1_micro'],
        'histgradientboostingclassifier__random_state': [42],
    }
    # instantiate the gridsearch
    hgb_grid = GridSearchCV(hgb_pipe, parameters, n_jobs=5, cv=5, scoring='f1_macro', verbose=2, refit=True)
    # fit on the grid
    hgb_grid.fit(X_train.values, y_train.values)

    model_HGB = hgb_grid.best_estimator_

    model_HGB.score(X_test.values, y_test.values)

    y_all = model_HGB.predict(X.values)
    full_report = classification_report(y.values, y_all)

    print(full_report)

    # Save the best estimator to a file
    with open('best_hgb_model.pkl', 'wb') as file:
        pickle.dump(model_HGB, file)

    return model_HGB
