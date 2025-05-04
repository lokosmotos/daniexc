from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import pandas as pd
from messaging import send_sms_reminder

app = Flask(__name__)
CORS(app)

# Mock database
candidates_db = []
interviews_db = []

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data.get('username') == 'syida' and data.get('password') == '8888':
        return jsonify({"success": True, "user": "Syida"})
    return jsonify({"success": False}), 401

@app.route('/candidates', methods=['GET', 'POST'])
def handle_candidates():
    if request.method == 'POST':
        candidate = request.json
        if not candidate.get('resume') and not candidate.get('no_resume_reason'):
            return jsonify({"error": "Resume or reason required"}), 400
        candidates_db.append(candidate)
        return jsonify({"success": True}), 201
    return jsonify(candidates_db)

@app.route('/interviews', methods=['POST'])
def schedule_interview():
    data = request.json
    interviews_db.append(data)
    send_sms_reminder(data['candidate_id'])
    return jsonify({"success": True})

@app.route('/export', methods=['GET'])
def export_data():
    df = pd.DataFrame(candidates_db)
    output = io.BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)
    return send_file(output, mimetype='application/vnd.ms-excel')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
