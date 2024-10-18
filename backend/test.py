from mining_patterns_charm import mining_patterns_CHARM 
import os


csv_file_path = os.path.abspath("../CSV_GeneratedFile/alertCSV.csv")

pattern_count, pattern_data = mining_patterns_CHARM(csv_file_path)

print(pattern_data)
