import pandas as pd
import os

from mining_patterns_charm import mining_patterns_CHARM 

csv_file_path = os.path.abspath("../CSV_GeneratedFile/alertCSV.csv")


print("working test python")
pattern_count, pattern_data = mining_patterns_CHARM(csv_file_path)

# print(pattern_data)
