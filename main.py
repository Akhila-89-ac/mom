from flask import Flask, jsonify
from file_processor import process_meeting_files

app = Flask(__name__)

@app.route('/process-meeting', methods=['GET'])
def process_meeting():
    result = process_meeting_files()
    
    if result["status"] == "success":
        return jsonify({"status": "success", "message": result["message"]}), 200
    else:
        return jsonify({"status": "error", "message": result["message"]}), 400

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
