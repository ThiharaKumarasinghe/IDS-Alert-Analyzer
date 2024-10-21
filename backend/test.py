from mining_patterns_charm import mining_patterns_CHARM 
import os

from XAI.XAI_functions import train_optimum_model, aggregate_lime_explanations

# Path to the cluster CSV file
cluster_csv_path = os.path.abspath("./clustering/cluster_data.csv")

# test
train_optimum_model(cluster_csv_path)

explanation = aggregate_lime_explanations(cluster_csv_path,6)

print(explanation)