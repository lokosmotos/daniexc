from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "🐾 HR Backend Online"

if __name__ == '__main__':
    app.run()
