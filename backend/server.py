from flask import Flask, request, jsonify   # type: ignore
import pandas as pd       # type: ignore
from flask_cors import CORS  # type: ignore
import os

app = Flask(__name__)

# Enable CORS for the entire Flask app
CORS(app)

# Endpoint to get the alert count
@app.route('/api/alert-count', methods=['GET'])
def get_alert_count():
    # Path to the CSV file
    csv_file_path = os.path.abspath("../CSV_GeneratedFile/4.csv")
    
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


if __name__ == '__main__':
    app.run(debug=True)
