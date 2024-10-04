from flask import Flask, request, jsonify, send_file  # type: ignore
import pandas as pd  # type: ignore
from flask_cors import CORS  # type: ignore
import os

app = Flask(__name__)

# Enable CORS for the entire Flask app
CORS(app)

# Path to the CSV file
csv_file_path = os.path.abspath("../CSV_GeneratedFile/alertCSV.csv")

# Endpoint to get the alert count--------------------------------------------------------------------------------------------------------------------------------
@app.route('/api/alert-count', methods=['GET'])
def get_alert_count():
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file_path)
        
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


if __name__ == '__main__':
    app.run(debug=True)
