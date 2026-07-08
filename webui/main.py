from flask import Flask, render_template
import os

app = Flask(__name__)


@app.route('/')
def index():
    postgrest_url = os.getenv("POSTGREST_URL", "http://localhost:3000")
    return render_template('index.html', postgrest_url=postgrest_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
