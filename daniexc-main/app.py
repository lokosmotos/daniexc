import os
from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_excel_to_srt():
    uploaded_file = request.files['excel']
    language = request.form['language']  # 'ov', 'spanish', or 'english'

    if not uploaded_file.filename.endswith(('.xlsx', '.xls')):
        return "Please upload a valid Excel file.", 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(filepath)

    # Load Excel
    try:
        df = pd.read_excel(filepath)
    except Exception as e:
        return f"Error reading Excel file: {e}", 400
    
    # Map selection to column
    language_map = {
        'ov': 'OV DIALOGUES',
        'spanish': 'SPANISH SUBTITLES',
        'english': 'ENGLISH SUBTITLES'
    }
    col = language_map.get(language)
    
    if col not in df.columns:
        return f"Column '{col}' not found in Excel.", 400

    # Create SRT
    lines = df[col].fillna('').tolist()
    srt_path = os.path.join(app.config['OUTPUT_FOLDER'], f'{language}.srt')

    with open(srt_path, 'w', encoding='utf-8') as f:
        for i, line in enumerate(lines, start=1):
            start_sec = i * 3
            end_sec = start_sec + 2
            f.write(f"{i}\n")
            f.write(f"00:00:{start_sec:02},000 --> 00:00:{end_sec:02},000\n")
            f.write(f"{line.strip()}\n\n")

    return send_from_directory(app.config['OUTPUT_FOLDER'], f'{language}.srt', as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
