from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    # Process the uploaded PCAP file here and generate a CSV
    # csv_file = convert_pcap_to_csv(file)

    # Perform analysis (dummy data for now)
    data = {'Feature': ['Tot Fwd Pkts', 'Flow Duration'], 'Value': [123, 456]}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
