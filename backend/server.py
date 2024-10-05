from flask import Flask, request, jsonify, send_file  # type: ignore
import pandas as pd  # type: ignore
from flask_cors import CORS  # type: ignore
import os

# import data mining code
from mining_patterns_charm import mining_patterns_CHARM 

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
csv_file_path = os.path.abspath("../CSV_GeneratedFile/alertCSV.csv")

# Path to the pattern CSV file
pattern_csv_path = os.path.abspath("./patterns/IDS_data_0.01_3Null_19features.csv")

# Endpoint to get the alert count--------------------------------------------------------------------------------------------------------------------------------
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


# Get all alert data from CSV----------------------------------------------------------------------------------------------------------------------------
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


# Endpoint to download the CSV file----------------------------------------------------------------------------------------------------------------------------
@app.route('/api/download-csv', methods=['GET'])
def download_csv():
    try:
        # Serve the CSV file as a downloadable attachment
        return send_file(csv_file_path, as_attachment=True, download_name='alert-data.csv', mimetype='text/csv')
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define a route to process the alert file and get the patterns-----------------------------------------------------------------------------------------------------
# Define a route to get patterns using the predefined CSV file path
@app.route('/api/get_patterns', methods=['GET'])
def get_patterns():
    try:
        # Call the mining_patterns_CHARM function with the CSV file path
        pattern_count, pattern_data = mining_patterns_CHARM(csv_file_path)

        # Return the pattern count and the pattern data as a JSON response
        return jsonify({
            "pattern_count": pattern_count,
            "pattern_data": pattern_data
        }), 200
    except FileNotFoundError:
        return jsonify({"error": "CSV file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500






if __name__ == '__main__':
    app.run(debug=True)
