from flask import Blueprint, request, jsonify
from controllers.movie_controller import (
    add_movie_controller,
    get_all_movies_controller,
    get_movie_controller,
    update_movie_controller,
    delete_movie_controller,
    get_top_rated_movies_controller,
)

movie_bp = Blueprint('movie', __name__)


# Create a new movie
@movie_bp.route('/movies', methods=['POST'])
def add_movie():
    data = request.get_json()
    result, status_code = add_movie_controller(data)
    return jsonify(result), status_code


# Get all movies
@movie_bp.route('/movies', methods=['GET'])
def get_movies():
    result, status_code = get_all_movies_controller()
    return jsonify(result), status_code


# Get a movie by ID
@movie_bp.route('/movies/<string:movie_id>', methods=['GET'])
def get_movie(movie_id):
    result, status_code = get_movie_controller(movie_id)
    return jsonify(result), status_code


# Update a movie
@movie_bp.route('/movies/<string:movie_id>', methods=['PUT'])
def update_a_movie(movie_id):
    data = request.get_json()
    result, status_code = update_movie_controller(movie_id, data)
    return jsonify(result), status_code


# Delete a movie
@movie_bp.route('/movies/<string:movie_id>', methods=['DELETE'])
def delete_a_movie(movie_id):
    result, status_code = delete_movie_controller(movie_id)
    return jsonify(result), status_code


# Get top rated movies
@movie_bp.route('/movies/top-rated', methods=['GET'])
def get_top_rated_movies():
    result, status_code = get_top_rated_movies_controller()
    return jsonify(result), status_code
