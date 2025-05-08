from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Initialize DB
def init_db():
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  position TEXT,
                  experience INTEGER,
                  status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add', methods=['GET', 'POST'])
def add_candidate():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        experience = request.form['experience']
        status = request.form['status']
        conn = sqlite3.connect('candidates.db')
        c = conn.cursor()
        c.execute("INSERT INTO candidates (name, position, experience, status) VALUES (?, ?, ?, ?)",
                  (name, position, experience, status))
        conn.commit()
        conn.close()
        return redirect(url_for('candidate_pool'))
    return render_template('add_candidate.html')

@app.route('/pool')
def candidate_pool():
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    c.execute("SELECT * FROM candidates")
    candidates = c.fetchall()
    conn.close()
    return render_template('candidate_pool.html', candidates=candidates)

@app.route('/edit/<int:candidate_id>', methods=['GET', 'POST'])
def edit_candidate(candidate_id):
    conn = sqlite3.connect('candidates.db')
    c = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        experience = request.form['experience']
        status = request.form['status']
        c.execute("UPDATE candidates SET name=?, position=?, experience=?, status=? WHERE id=?",
                  (name, position, experience, status, candidate_id))
        conn.commit()
        conn.close()
        return redirect(url_for('candidate_pool'))
    else:
        c.execute("SELECT * FROM candidates WHERE id=?", (candidate_id,))
        candidate = c.fetchone()
        conn.close()
        return render_template('edit_candidate.html', candidate=candidate)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

