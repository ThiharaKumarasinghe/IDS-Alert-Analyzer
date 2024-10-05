import pandas as pd  # type: ignore
import os

from mining_patterns_charm import mining_patterns_CHARM 
from clustering_hierarchical import hierarchical_clustering_using_patterns

csv_file_path = os.path.abspath("../CSV_GeneratedFile/alertCSV.csv")
pattern_csv_path = os.path.abspath("./patterns/IDS_data_0.01_3Null_19features.csv")

df = hierarchical_clustering_using_patterns(pattern_csv_path)

print(df)


# print(pattern_data)
