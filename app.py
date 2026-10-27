from flask import Flask
from flask_cors import CORS
from config import client
from routes.movie_routes import movie_bp
from routes.review_routes import review_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(movie_bp, url_prefix='/api')
app.register_blueprint(review_bp, url_prefix='/api')

@app.route('/health', methods=['GET'])
def health():
    try:
        client.admin.command('ping')
        return{
            "message": " MongoDB connected successfully"
        },200
    except Exception as error:
        return {
            "error": str(error)
        }, 500


if __name__ == '__main__':
    app.run(debug=True)