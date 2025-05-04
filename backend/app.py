from flask import Flask, request, jsonify, send_file
import os
from datetime import datetime, timedelta
from messaging import (
    send_interview_reminder,
    send_no_show_alert,
    send_standby_inquiry
)

# ... (previous imports and setup)

@app.route('/candidates', methods=['POST'])
def add_candidate():
    data = request.json
    if not data.get('resume_url') and not data.get('no_resume_reason'):
        return jsonify({"error": "Resume URL or reason required"}), 400
    
    # Validate Google Drive URL
    if data.get('resume_url') and 'drive.google.com' not in data['resume_url']:
        return jsonify({"error": "Only Google Drive links accepted"}), 400
    
    candidate = {
        **data,
        "created_at": datetime.now().isoformat(),
        "status": "New"
    }
    candidates_db.append(candidate)
    return jsonify({"success": True}), 201

@app.route('/send-bulk-messages', methods=['POST'])
def bulk_messaging():
    message_type = request.json.get('type')
    candidate_ids = request.json.get('candidate_ids', [])
    
    for candidate_id in candidate_ids:
        candidate = next((c for c in candidates_db if c['id'] == candidate_id), None)
        if candidate:
            if message_type == 'interview_reminder':
                send_interview_reminder(candidate)
            elif message_type == 'no_show':
                send_no_show_alert(candidate)
            elif message_type == 'standby':
                send_standby_inquiry(candidate)
    
    return jsonify({"success": True, "sent_count": len(candidate_ids)})
