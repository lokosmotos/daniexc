from flask import Flask, render_template, request, redirect, session, send_file
import pandas as pd
import os
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'your_secret_key'

PASSWORD = "dan123"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect('/upload')
        else:
            return "Wrong password. Try again."
    return render_template("login.html")

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect('/')
    if request.method == 'POST':
        file = request.files['file']
        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
            srt = convert_to_srt(df)
            return send_file(BytesIO(srt.encode('utf-8')),
                             download_name="output.srt",
                             as_attachment=True)
    return render_template("upload.html")

def convert_to_srt(df):
    srt = ""
    for i, row in df.iterrows():
        start = row.get("start", "00:00:00,000")
        end = row.get("end", "00:00:00,000")
        text = row.get("text", "")
        srt += f"{i+1}\n{start} --> {end}\n{text}\n\n"
    return srt

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
