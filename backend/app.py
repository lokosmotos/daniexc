from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def dashboard():
    # Sample data - replace with your actual database queries
    stats = {
        'total': 0,
        'hired': 0,
        'scheduled': 0
    }
    candidates = []  # Empty list for now
    return render_template('dashboard.html', stats=stats, candidates=candidates)

if __name__ == '__main__':
    app.run(debug=True)
