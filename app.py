from flask import Flask, render_template
from flask_cors import CORS

from config import get_client
from routes.movie_routes import movie_bp
from routes.review_routes import review_bp

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html'), 200


app.register_blueprint(movie_bp, url_prefix='/api')
app.register_blueprint(review_bp, url_prefix='/api')


@app.route('/health', methods=['GET'])
def health():
    try:
        get_client().admin.command('ping')
        return {
            "message": "MongoDB connected successfully"
        }, 200
    except Exception as error:
        return {
            "error": str(error)
        }, 500

import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)