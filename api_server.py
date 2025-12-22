from flask import Flask, jsonify
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/update-data', methods=['POST'])
def update_data():
    try:
        # Run fetch_pcso_data.py
        print("Running fetch_pcso_data.py...")
        result1 = subprocess.run(['python', 'fetch_pcso_data.py'], 
                                capture_output=True, 
                                text=True, 
                                timeout=60)
        
        # Run import_csv.py
        print("Running import_csv.py...")
        result2 = subprocess.run(['python', 'import_csv.py'], 
                                capture_output=True, 
                                text=True, 
                                timeout=60)
        
        # Check if files exist
        data_exists = os.path.exists('pcso_lotto_data.json')
        stats_exists = os.path.exists('pcso_statistics.json')
        
        return jsonify({
            'success': True,
            'message': 'Data updated successfully',
            'files_created': {
                'pcso_lotto_data.json': data_exists,
                'pcso_statistics.json': stats_exists
            },
            'fetch_output': result1.stdout,
            'import_output': result2.stdout
        })
    except subprocess.TimeoutExpired:
        return jsonify({
            'success': False,
            'error': 'Script execution timed out'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
