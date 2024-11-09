import pandas as pd  # type: ignore
import matplotlib.pyplot as plt # type: ignore
from sklearn.metrics import silhouette_score  # type: ignore
from sklearn.metrics import pairwise_distances  # type: ignore
from sklearn.preprocessing import LabelEncoder, OrdinalEncoder, StandardScaler  # type: ignore
import numpy as np
from sklearn.cluster import AgglomerativeClustering  # type: ignore
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import seaborn as sns  # type: ignore
import json

from clustering_functions import generate_floats_between, plot_graph_evaluate

def hierarchical_clustering_using_patterns(pattern_file_location,sillouette_threshold):
    df = pd.read_csv(pattern_file_location)
    print(df.head(10))
    print(df.info())
    # print(df['Label'].value_counts())

    patterns_with_NaN = df.iloc[:, 1:23]

    duplicate_pattern_count = patterns_with_NaN.duplicated().value_counts()
    print(f"\n\nduplicate_pattern_count :{duplicate_pattern_count}")

    null_handled_patterns = patterns_with_NaN.copy()
    null_handled_patterns = null_handled_patterns.astype(float)
    # numerical_cols = null_handled_patterns.select_dtypes(include=['float64', 'int64']).columns
    # categorical_cols = null_handled_patterns.select_dtypes(include=['object']).columns

    # Open the JSON file and load the data
    with open('categorization.json', 'r') as file:
        data = json.load(file)

    # Extract column names from the loaded data
    numerical_cols = [item[0] for item in data]

    all_columns = null_handled_patterns.columns.to_list()
    categorical_cols = list(set(all_columns) - set(numerical_cols))

    print(numerical_cols)
    print(categorical_cols)

    for idx, column in enumerate(null_handled_patterns.columns):
        print(null_handled_patterns[column].min())

    for idx, column in enumerate(null_handled_patterns.columns):
        null_handled_patterns[column] = null_handled_patterns[column].fillna(-1)

    # print(null_handled_patterns.info())

    null_handled_patterns_encoded = pd.DataFrame(null_handled_patterns, columns=null_handled_patterns.columns)

    label_encoders = {}
    for col in categorical_cols:
        le = LabelEncoder()
        null_handled_patterns_encoded[col] = le.fit_transform(null_handled_patterns[col])
        label_encoders[col] = le

    # print("\nDataFrame after encoding categorical features:")
    # print(null_handled_patterns_encoded.head(20))

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(null_handled_patterns_encoded)
    null_handled_patterns_encoded = pd.DataFrame(scaled_data, columns=null_handled_patterns_encoded.columns)

    # Convert DataFrame to numpy array for K-Prototypes
    data_matrix = null_handled_patterns_encoded.values

    # print(data_matrix)

    # Define methods and metrics
    methods = ['complete', 'average', 'single']
    metrics = ['euclidean', 'jaccard', 'cosine']

    # # Create a 3x3 subplot for the dendrograms
    # fig, axes = plt.subplots(3, 3, figsize=(15, 15))
    #
    # # Loop through methods and metrics to generate dendrograms
    # for i, method in enumerate(methods):
    #     for j, metric in enumerate(metrics):
    #         # Perform hierarchical clustering
    #         Z = linkage(data_matrix, method=method, metric=metric)
    #
    #         # Plot dendrogram
    #         ax = axes[i, j]
    #         dendrogram(Z, orientation='top', distance_sort='descending', show_leaf_counts=False, ax=ax)
    #         ax.set_title(f'Method: {method}, Metric: {metric}')
    #         ax.set_xlabel('Sample index')
    #         ax.set_ylabel('Distance')
    #
    # # Adjust layout for better visualization
    # plt.tight_layout()
    # plt.show()

    # Initialize the DataFrame and score data list
    score_df = pd.DataFrame(columns=['metric', 'linkage', 'number of clusters', 'accuracy_score',
                                    'v_measure_score', 'silhouette_score', 'davies_bouldin_score'])
    score_data = []

    for affinity in metrics:
        for linkage_method in methods:
            # Perform hierarchical clustering
            Z = linkage(data_matrix, method=linkage_method, metric=affinity)

            # Extract distances
            distances = Z[:, 2]

            # Get the minimum and maximum distances
            min_distance = np.min(distances)
            max_distance = np.max(distances)

            list_of_distances = generate_floats_between(min_distance, max_distance)
            # print(list_of_distances)

            for n_distance in list_of_distances:
                clusters = fcluster(Z, t=n_distance, criterion='distance')
                n_clusters = len(set(clusters))  # Calculate the number of clusters
                # print(
                #     f"-----------------------------{n_distance, n_clusters, affinity, linkage_method}--------------------------------------")

                if n_clusters == len(df):
                    # print(f"Skipping. number of clusters are {n_clusters}")
                    continue

                if n_clusters == 1:
                    # print(f"Skipping. number of clusters are {n_clusters}")
                    continue

                # Evaluate the clustering performance
                silouette = plot_graph_evaluate(clusters, null_handled_patterns, null_handled_patterns_encoded, df)

                # Append the evaluation results to score_data
                score_data.append({
                    'metric': affinity,
                    'linkage': linkage_method,
                    'number of clusters': n_clusters,
                    # 'accuracy_score': acc_score,
                    # 'v_measure_score': v_measure,
                    'silhouette_score': silouette,
                    # 'davies_bouldin_score': davisB_score
                })

    # Convert the list of dictionaries to a DataFrame
    score_df = pd.DataFrame(score_data)
    cosine_metric = score_df[score_df['metric'] == 'cosine']
    average_cosine = cosine_metric[cosine_metric['linkage'] == 'average']
    print(average_cosine)
    # num_optimum_clusters = average_cosine[average_cosine['silhouette_score']>sillouette_threshold].iloc[-1]['number of clusters']

    filtered_avg_cosine = average_cosine[average_cosine['silhouette_score'] > sillouette_threshold]

    if not filtered_avg_cosine.empty:
        # Get the number of clusters from the last row that matches the condition
        num_optimum_clusters = filtered_avg_cosine.iloc[-1]['number of clusters']
    else:
        # Get the number of clusters with the maximum silhouette score
        num_optimum_clusters = average_cosine.loc[average_cosine['silhouette_score'].idxmax()]['number of clusters']
        print(f"No clusters met the threshold. Using the maximum silhouette {average_cosine.loc[average_cosine['silhouette_score'].idxmax()]['silhouette_score']} score instead.")

    print(f"Selected num_optimum_clusters: {num_optimum_clusters}")

    hierarchical_clustering = AgglomerativeClustering(n_clusters=num_optimum_clusters,
                                                    metric='cosine',
                                                    linkage='average')
    clusters = hierarchical_clustering.fit_predict(data_matrix)

    print("\n======== Optimum Clusters Data==========")

    plot_graph_evaluate(clusters, null_handled_patterns, null_handled_patterns_encoded, df)

    # Z = linkage(data_matrix, method='average', metric='cosine')
    # clusters = fcluster(Z, t=num_optimum_clusters, criterion='maxclust')
    print(set(clusters))
    # plot_graph_evaluate(clusters, null_handled_patterns, null_handled_patterns_encoded, df)


    df['cluster'] = clusters

    df.to_csv('./clustering/cluster_data.csv', index=False)

    return df
