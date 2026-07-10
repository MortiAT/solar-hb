from flask import Flask, render_template
import os

class DevelopmentConfig:  
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig) 

@app.route('/')
def index():
    postgrest_url = os.getenv("POSTGREST_URL", "http://localhost:3000")
    return render_template('index.html', postgrest_url=postgrest_url)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
