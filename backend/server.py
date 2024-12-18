from flask import Flask, request, jsonify, send_file  # type: ignore
import pandas as pd  # type: ignore
from flask_cors import CORS  # type: ignore
import os
import threading
import numpy as np
import subprocess
from dotenv import load_dotenv # type: ignore
load_dotenv()


# Add AI explanation
import google.generativeai as genai # type: ignore
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)


# import data mining code
from mining_patterns_charm import mining_patterns_CHARM 

# import data cluster code
from clustering_hierarchical import hierarchical_clustering_using_patterns

# import XAI code
from XAI.XAI_functions import train_optimum_model, aggregate_lime_explanations


# Dictionary for remane table features
rename_dict = {
    'src_ip': 'Src IP',
    'dst_ip': 'Dst IP',
    'src_port': 'Src Port',
    'dst_port': 'Dst Port',
    'protocol': 'Protocol',
    'timestamp': 'Timestamp',
    'flow_duration': 'Flow Duration',
    'flow_byts_s': 'Flow Byts/s',
    'flow_pkts_s': 'Flow Pkts/s',
    'fwd_pkts_s': 'Fwd Pkts/s',
    'bwd_pkts_s': 'Bwd Pkts/s',
    'tot_fwd_pkts': 'Tot Fwd Pkts',
    'tot_bwd_pkts': 'Tot Bwd Pkts',
    'totlen_fwd_pkts': 'TotLen Fwd Pkts',
    'totlen_bwd_pkts': 'TotLen Bwd Pkts',
    'fwd_pkt_len_max': 'Fwd Pkt Len Max',
    'fwd_pkt_len_min': 'Fwd Pkt Len Min',
    'fwd_pkt_len_mean': 'Fwd Pkt Len Mean',
    'fwd_pkt_len_std': 'Fwd Pkt Len Std',
    'bwd_pkt_len_max': 'Bwd Pkt Len Max',
    'bwd_pkt_len_min': 'Bwd Pkt Len Min',
    'bwd_pkt_len_mean': 'Bwd Pkt Len Mean',
    'bwd_pkt_len_std': 'Bwd Pkt Len Std',
    'pkt_len_max': 'Pkt Len Max',
    'pkt_len_min': 'Pkt Len Min',
    'pkt_len_mean': 'Pkt Len Mean',
    'pkt_len_std': 'Pkt Len Std',
    'pkt_len_var': 'Pkt Len Var',
    'fwd_header_len': 'Fwd Header Len',
    'bwd_header_len': 'Bwd Header Len',
    'fwd_seg_size_min': 'Fwd Seg Size Min',
    'fwd_act_data_pkts': 'Fwd Act Data Pkts',
    'flow_iat_mean': 'Flow IAT Mean',
    'flow_iat_max': 'Flow IAT Max',
    'flow_iat_min': 'Flow IAT Min',
    'flow_iat_std': 'Flow IAT Std',
    'fwd_iat_tot': 'Fwd IAT Tot',
    'fwd_iat_max': 'Fwd IAT Max',
    'fwd_iat_min': 'Fwd IAT Min',
    'fwd_iat_mean': 'Fwd IAT Mean',
    'fwd_iat_std': 'Fwd IAT Std',
    'bwd_iat_tot': 'Bwd IAT Tot',
    'bwd_iat_max': 'Bwd IAT Max',
    'bwd_iat_min': 'Bwd IAT Min',
    'bwd_iat_mean': 'Bwd IAT Mean',
    'bwd_iat_std': 'Bwd IAT Std',
    'fwd_psh_flags': 'Fwd PSH Flags',
    'bwd_psh_flags': 'Bwd PSH Flags',
    'fwd_urg_flags': 'Fwd URG Flags',
    'bwd_urg_flags': 'Bwd URG Flags',
    'fin_flag_cnt': 'FIN Flag Cnt',
    'syn_flag_cnt': 'SYN Flag Cnt',
    'rst_flag_cnt': 'RST Flag Cnt',
    'psh_flag_cnt': 'PSH Flag Cnt',
    'ack_flag_cnt': 'ACK Flag Cnt',
    'urg_flag_cnt': 'URG Flag Cnt',
    'ece_flag_cnt': 'ECE Flag Cnt',
    'down_up_ratio': 'Down/Up Ratio',
    'pkt_size_avg': 'Pkt Size Avg',
    'init_fwd_win_byts': 'Init Fwd Win Byts',
    'init_bwd_win_byts': 'Init Bwd Win Byts',
    'active_max': 'Active Max',
    'active_min': 'Active Min',
    'active_mean': 'Active Mean',
    'active_std': 'Active Std',
    'idle_max': 'Idle Max',
    'idle_min': 'Idle Min',
    'idle_mean': 'Idle Mean',
    'idle_std': 'Idle Std',
    'fwd_byts_b_avg': 'Fwd Byts/b Avg',
    'fwd_pkts_b_avg': 'Fwd Pkts/b Avg',
    'bwd_byts_b_avg': 'Bwd Byts/b Avg',
    'bwd_pkts_b_avg': 'Bwd Pkts/b Avg',
    'fwd_blk_rate_avg': 'Fwd Blk Rate Avg',
    'bwd_blk_rate_avg': 'Bwd Blk Rate Avg',
    'fwd_seg_size_avg': 'Fwd Seg Size Avg',
    'bwd_seg_size_avg': 'Bwd Seg Size Avg',
    'cwe_flag_count': 'CWE Flag Count',
    'subflow_fwd_pkts': 'Subflow Fwd Pkts',
    'subflow_bwd_pkts': 'Subflow Bwd Pkts',
    'subflow_fwd_byts': 'Subflow Fwd Byts',
    'subflow_bwd_byts': 'Subflow Bwd Byts'
}

app = Flask(__name__)

# Enable CORS for the entire Flask app
CORS(app)

# Path to the CSV file
csv_file_path = os.path.abspath("./Generated_CSV/alertCSV.csv")

# Path to the pattern CSV file
pattern_csv_path = os.path.abspath("./patterns/IDS_data_0.01_3Null_19features.csv")

# Path to the cluster CSV file
cluster_csv_path = os.path.abspath("./clustering/cluster_data.csv")

# Path to the mapped patterns
mappedPattern_csv_path = os.path.abspath('./patterns/mapped/mappedPatterns.csv')

# Global variable to track the training status
training_status = {
    "is_training": False
}

# Endpoint to get the alert count
@app.route('/api/alert-count', methods=['GET'])
def get_alert_count():
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        # Rename the columns
        df.rename(columns=rename_dict, inplace=True)

        # Save the modified DataFrame to a new CSV file (or replace the existing one)
        df.to_csv(csv_file_path, index=False)

        # Assuming each row in the CSV file represents an alert
        alert_count = len(df)
        
        
        # Return the alert count as JSON response
        return jsonify({"alertCount": alert_count}), 200
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get all alert data from CSV
@app.route('/api/csv-data-alert', methods=['GET'])
def get_csv_data():
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file_path)
        
        # Convert DataFrame to a list of dictionaries (for JSON serialization)
        csv_data = df.to_dict(orient='records')
        
        # Return the CSV data as JSON response
        return jsonify(csv_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Endpoint to download the CSV file
@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    try:
        # Serve the CSV file as a downloadable attachment
        return send_file(csv_file_path, as_attachment=True, download_name='alert-data.csv', mimetype='text/csv')
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define a route to get patterns using the predefined CSV file path
@app.route('/api/get_patterns', methods=['GET'])
def get_patterns():
    try:
        # Call the mining_patterns_CHARM function with the CSV file path
        pattern_count, pattern_data = mining_patterns_CHARM(csv_file_path)



        # Print pattern count to the console
        print(f"Pattern count: {type(pattern_count)}")
        print(f"Pattern count: {pattern_data}")
        # print(f"Pattern data: {pattern_data}")

        # Return the pattern count and the pattern data as a JSON response
        return jsonify({
            "pattern_count": pattern_count,
            "pattern_data": pattern_data
        }), 200

    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Get all clusters from patterns based on silhouette score
@app.route('/api/get-clusters', methods=['GET'])
def get_cluster_data():
    try:
        # Get the silhouette score from the query parameters
        silhouette_score = float(request.args.get('score', 0.8))  # Default value of 0.8 if not provided
        
        # Call the clustering function with the silhouette score
        df = hierarchical_clustering_using_patterns(pattern_csv_path, silhouette_score)
        
        # Group the data by 'cluster' to calculate the required information
        cluster_summary = df.groupby('cluster').agg(
            pattern_count=('cluster', 'size'),             # Count of patterns in each cluster
            total_alerts=('Support Count', 'sum')          # Summation of Support Count (alerts) in each cluster
        ).reset_index()
        
        # Convert to a list of dictionaries (for JSON serialization)
        cluster_data = cluster_summary.to_dict(orient='records')
        
        # Return the cluster data as JSON response
        return jsonify(cluster_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# Get pattern details in given cluster
@app.route('/api/cluster/<cluster_name>/patterns', methods=['GET'])
def get_cluster_patterns(cluster_name):
    try:
        # Convert the cluster_name from string to integer
        cluster_name_int = int(cluster_name)
        
        # Read the CSV file into a DataFrame
        df = pd.read_csv(cluster_csv_path)
        
        # Filter the DataFrame by the given cluster name (as integer)
        filtered_cluster = df[df['cluster'] == cluster_name_int]
        
        if filtered_cluster.empty:
            return jsonify({"error": "Cluster not found"}), 404
        
        # Get pattern count and alert count (sum of Support Count)
        pattern_count = int(len(filtered_cluster))  # Convert to int
        alert_count = int(filtered_cluster['Support Count'].sum())  # Convert to int
        
        # Convert the filtered data to a list of dictionaries
        pattern_data = filtered_cluster.to_dict(orient='records')
        
        # Replace NaN values with None (which will be serialized as null in JSON)
        for pattern in pattern_data:
            for key, value in pattern.items():
                if isinstance(value, (np.int64, np.float64)):  # Check for NumPy types
                    pattern[key] = value.item()  # Convert to Python native type
                elif pd.isna(value):  # Check for NaN values
                    pattern[key] = None  # Replace NaN with None
        
        # Return the pattern data, pattern count, and alert count as JSON response
        return jsonify({
            "cluster_name": cluster_name_int,
            "pattern_count": pattern_count,
            "alert_count": alert_count,
            "pattern_data": pattern_data
        }), 200
    
    except ValueError:
        return jsonify({"error": "Invalid cluster name, must be an integer"}), 400
    except FileNotFoundError:
        return jsonify({"error": "Cluster CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Get all clusters from patterns
@app.route('/api/get-clusters-back', methods=['GET'])
def get_cluster_data_back():
    try:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(cluster_csv_path)
        
        # Group the data by 'cluster' to calculate the required information
        cluster_summary = df.groupby('cluster').agg(
            pattern_count=('cluster', 'size'),             # Count of patterns in each cluster
            total_alerts=('Support Count', 'sum')          # Summation of Support Count (alerts) in each cluster
        ).reset_index()
        
        # Convert to a list of dictionaries (for JSON serialization)
        cluster_data = cluster_summary.to_dict(orient='records')
        
        # Return the cluster data as JSON response
        return jsonify(cluster_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


# XAI routes---------------------------------------------------------

# train the XAI model
@app.route('/api/train-xai-model', methods=['GET'])
def train_xai_model():
    global training_status

    # If a model is already being trained, return status
    if training_status["is_training"]:
        return jsonify({"message": "Model training is already in progress"}), 200

    # Set the status to indicate that training has started
    training_status["is_training"] = True

    # Start a new thread for training the model
    model_accuracy = train_optimum_model(cluster_csv_path)
    # thread = threading.Thread(target=train_optimum_model, args=(cluster_csv_path))
    # thread.start()
    training_status["is_training"] = False

    return jsonify({ "message": "Model training completed", "accuracy": model_accuracy }), 202

@app.route('/api/training-status', methods=['GET'])
def get_training_status():
    global training_status
    return jsonify({"is_training": training_status["is_training"]}), 200


@app.route('/api/cluster/<cluster_name>/xai', methods=['GET'])
def aggregate_lime_explanations_route(cluster_name):
    try:
        # Convert the cluster_name from string to integer
        cluster_name_int = int(cluster_name)
        print(cluster_name_int)
        
        if not cluster_name_int:
            return jsonify({"error": "Cluster name is required"}), 400
        
        # Run aggregate_lime_explanations for the given clusterName
        explanation_output = aggregate_lime_explanations(cluster_csv_path, cluster_name_int)
        print(explanation_output)
        
        # Return the result to the frontend
        return jsonify({"result": explanation_output}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PCAP file uploading----------------------------------------------------------------------------------------------------------------------------
# Directory to save uploaded files
UPLOAD_FOLDER = './uploads'
GENERATED_CSV_FOLDER = './Generated_CSV'

# Ensure that the directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GENERATED_CSV_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():

    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    if not file.filename.endswith('.pcap'):
        return jsonify({'message': 'Invalid file format. Please upload a .pcap file'}), 400

    # Save the file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Convert the .pcap file to .csv using CICFlowMeter
    try:
        csv_output_path = os.path.join(GENERATED_CSV_FOLDER, "alertCSV.csv")
        # Define the path to your virtual environment's activation script
        venv_activation = os.path.join(".venv", "Scripts", "activate.bat")

        # Command to run within the virtual environment
        command = f'cmd.exe /c "{venv_activation} && cicflowmeter -f \"{file_path}\" -c \"{csv_output_path}\""'
        
        # cicflowmeter_command = [
        #     'CICFlowMeter',
        #     '-f', os.path.abspath(file_path),
        #     '-c', os.path.abspath(csv_output_path)
        # ]

        # Run the CICFlowMeter command
        subprocess.run(command, check=True)

        return jsonify({'message': f'File converted successfully. CSV saved at {csv_output_path}'}), 200

    except Exception as e:
        return jsonify({'message': f'Error processing file: {str(e)}'}), 500


# get Gemini explanation

@app.route('/api/explain-cluster', methods=['POST'])
def explain_cluster():
    try:
        # print(GEMINI_API_KEY)

        # Get the cluster result from the request
        cluster_result = request.json.get('cluster_result', None)
        if not cluster_result:
            return jsonify({"error": "No cluster result provided"}), 400

        # print(cluster_result)
        generation_config = {
        "temperature": 0.3,
        "top_p": 0.5,
        "top_k": 64,
        # "max_output_tokens": 500,
        # "response_mime_type": "text/plain",
        }
        # Initialize the Gemini model
        # model = genai.GenerativeModel("gemini-1.5-flash")
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )
                
        # Generate the explanation using Gemini API
        # promt = "Explain the following cluster result in terms of network traffic analysis:"
        protocol_dict = {
            0: "HOPOPT",
            1: "ICMP",
            2: "IGMP",
            3: "GGP",
            4: "IPv4",
            5: "ST",
            6: "TCP",
            7: "CBT",
            8: "EGP",
            9: "IGP",
            10: "BBN-RCC-MON",
            11: "NVP-II",
            12: "PUP",
            13: "ARGUS (deprecated)",
            14: "EMCON",
            15: "XNET",
            16: "CHAOS",
            17: "UDP",
            18: "MUX",
            19: "DCN-MEAS",
            20: "HMP",
            21: "PRM",
            22: "XNS-IDP",
            23: "TRUNK-1",
            24: "TRUNK-2",
            25: "LEAF-1",
            26: "LEAF-2",
            27: "RDP",
            28: "IRTP",
            29: "ISO-TP4",
            30: "NETBLT",
            31: "MFE-NSP",
            32: "MERIT-INP",
            33: "DCCP",
            34: "3PC",
            35: "IDPR",
            36: "XTP",
            37: "DDP",
            38: "IDPR-CMTP",
            39: "TP++",
            40: "IL",
            41: "IPv6",
            42: "SDRP",
            43: "IPv6-Route",
            44: "IPv6-Frag",
            45: "IDRP",
            46: "RSVP",
            47: "GRE",
            48: "DSR",
            49: "BNA",
            50: "ESP",
            51: "AH",
            52: "I-NLSP",
            53: "SWIPE (deprecated)",
            54: "NARP",
            55: "Min-IPv4",
            56: "TLSP",
            57: "SKIP",
            58: "IPv6-ICMP",
            59: "IPv6-NoNxt",
            60: "IPv6-Opts",
            61: "any host internal protocol",
            62: "CFTP",
            63: "any local network",
            64: "SAT-EXPAK",
            65: "KRYPTOLAN",
            66: "RVD",
            67: "IPPC",
            68: "any distributed file system",
            69: "SAT-MON",
            70: "VISA",
            71: "IPCV",
            72: "CPNX",
            73: "CPHB",
            74: "WSN",
            75: "PVP",
            76: "BR-SAT-MON",
            77: "SUN-ND",
            78: "WB-MON",
            79: "WB-EXPAK",
            80: "ISO-IP",
            81: "VMTP",
            82: "SECURE-VMTP",
            83: "VINES",
            84: "IPTM",
            85: "NSFNET-IGP",
            86: "DGP",
            87: "TCF",
            88: "EIGRP",
            89: "OSPFIGP",
            90: "Sprite-RPC",
            91: "LARP",
            92: "MTP",
            93: "AX.25",
            94: "IPIP",
            95: "MICP (deprecated)",
            96: "SCC-SP",
            97: "ETHERIP",
            98: "ENCAP",
            99: "any private encryption scheme",
            100: "GMTP",
            101: "IFMP",
            102: "PNNI",
            103: "PIM",
            104: "ARIS",
            105: "SCPS",
            106: "QNX",
            107: "A/N",
            108: "IPComp",
            109: "SNP",
            110: "Compaq-Peer",
            111: "IPX-in-IP",
            112: "VRRP",
            113: "PGM",
            114: "any 0-hop protocol",
            115: "L2TP",
            116: "DDX",
            117: "IATP",
            118: "STP",
            119: "SRP",
            120: "UTI",
            121: "SMP",
            122: "SM (deprecated)",
            123: "PTP",
            124: "ISIS over IPv4",
            125: "FIRE",
            126: "CRTP",
            127: "CRUDP",
            128: "SSCOPMCE",
            129: "IPLT",
            130: "SPS",
            131: "PIPE",
            132: "SCTP",
            133: "FC",
            134: "RSVP-E2E-IGNORE",
            135: "Mobility Header",
            136: "UDPLite",
            137: "MPLS-in-IP",
            138: "manet",
            139: "HIP",
            140: "Shim6",
            141: "WESP",
            142: "ROHC",
            143: "Ethernet",
            144: "AGGFRAG",
            145: "NSH",
            146: "Homa",
            147: "Unassigned",
            # Additional unassigned values up to 252
            253: "Use for experimentation and testing",
            254: "Use for experimentation and testing"
        }

        prompt = (
            "Explain the following cluster result in terms of network traffic analysis. Please note that these traffic might contain data related both malecious traffic and benign traffic:\n"
            "Use the following dictionary to intercept protocol values in cluster data:\n"
            f"{protocol_dict}\n"
            f"{cluster_result}"
        )

        response = model.generate_content(prompt)
        
        # Extract the explanation text from the response
        explanation = response.text.strip()  # Assuming `response.text` contains the explanation

        # print(explanation)  # Log the explanation for debugging

        # Return the explanation to the frontend as JSON
        return jsonify({"explanation": explanation})

    except Exception as e:
        return jsonify({"error": str(e)}), 500












































if __name__ == '__main__':
    app.run(debug=True)
