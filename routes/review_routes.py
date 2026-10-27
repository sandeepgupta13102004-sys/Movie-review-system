from flask import Blueprint, jsonify, request
from controllers.review_controller import add_review_controller, get_reviews_controller

review_bp = Blueprint('reviews', __name__)


@review_bp.route('/movies/<string:movie_id>/reviews', methods=['POST'])
def add_review(movie_id):
    data = request.get_json()
    result, status_code = add_review_controller(movie_id, data)
    return jsonify(result), status_code


@review_bp.route('/movies/<string:movie_id>/reviews', methods=['GET'])
def get_reviews(movie_id):
    result, status_code = get_reviews_controller(movie_id)
    return jsonify(result), status_code


def test_review():
    return jsonify({'message': 'Review route is working!'}), 200