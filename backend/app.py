from flask import Flask, request, jsonify
from datetime import datetime, timedelta
from messaging import (
    send_interview_reminder,
    send_no_show_alert,
    send_standby_inquiry
)

app = Flask(__name__)

# Temporary in-memory database (you can later replace with real DB)
candidates_db = []

@app.route('/candidates', methods=['POST'])
def add_candidate():
    data = request.json
    if not all(k in data for k in ('name', 'email', 'phone', 'position', 'interview_time', 'branch')):
        return jsonify({'error': 'Missing required fields'}), 400

    candidate = {
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'position': data['position'],
        'interview_time': data['interview_time'],
        'branch': data['branch']
    }
    candidates_db.append(candidate)

    # Send interview reminder
    email_sent = send_interview_reminder(candidate)
    if not email_sent:
        return jsonify({'error': 'Failed to send interview reminder'}), 500

    return jsonify({'message': 'Candidate added and reminder sent'}), 201


@app.route('/send-bulk-messages', methods=['POST'])
def send_bulk_messages():
    today = datetime.now()
    no_show_cutoff = today - timedelta(days=1)

    no_shows = []
    standbys = []

    for candidate in candidates_db:
        interview_time = datetime.fromisoformat(candidate['interview_time'])
        if interview_time.date() == no_show_cutoff.date():
            no_shows.append(candidate)
        elif candidate['position'].lower() == 'part-time':
            standbys.append(candidate)

    # Send no-show alerts
    no_show_results = [send_no_show_alert(c) for c in no_shows]

    # Send standby inquiries
    standby_results = [send_standby_inquiry(c) for c in standbys]

    return jsonify({
        'no_shows_contacted': len([r for r in no_show_results if r]),
        'standbys_contacted': len([r for r in standby_results if r])
    })


@app.route('/')
def index():
    return 'Candidate Messaging API is running 🚀'


if __name__ == '__main__':
    app.run(debug=True)
