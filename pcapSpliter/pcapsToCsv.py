import os
import subprocess

# split largr pcap into small
#editcap -c 1000000 pacpLarge.pcap split_file.pcap
#python pcapsToCsv.py

# Path to the folder containing the split PCAP files
pcap_directory = './pcaps'  # Update this to the correct directory

# Output directory for CSV files
csv_output_directory = './csv'  # Update this to where you want the CSVs saved

# Create output directory if it doesn't exist
if not os.path.exists(csv_output_directory):
    os.makedirs(csv_output_directory)

# Loop through all files in the directory
for filename in os.listdir(pcap_directory):
    if filename.endswith(".pcap"):
        # Get full path to the current PCAP file
        pcap_file_path = os.path.join(pcap_directory, filename)
        
        # Create the output CSV file name
        csv_filename = filename.replace('.pcap', '.csv')
        csv_file_path = os.path.join(csv_output_directory, csv_filename)
        
        # Run cicflowmeter command
        print(f"Converting {filename} to CSV...")
        command = f"cicflowmeter -f {pcap_file_path} -c {csv_file_path}"
        
        # Execute the command
        try:
            subprocess.run(command, shell=True, check=True)
            print(f"Successfully converted {filename} to {csv_filename}")
        except subprocess.CalledProcessError as e:
            print(f"Error converting {filename}: {e}")
