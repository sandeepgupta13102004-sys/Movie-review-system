from datetime import datetime
from bson import ObjectId
from config import movies_collection, reviews_collection


def serialize_movie(movie):
    if movie is None:
        return None

    serialized = dict(movie)
    if '_id' in serialized:
        serialized['id'] = str(serialized.pop('_id'))
    if 'release_date' in serialized and isinstance(serialized['release_date'], datetime):
        serialized['release_date'] = serialized['release_date'].strftime('%Y-%m-%d')
    if 'movie_id' in serialized and isinstance(serialized['movie_id'], ObjectId):
        serialized['movie_id'] = str(serialized['movie_id'])
    return serialized


# Create movie
def add_movie_controller(data):
    if not data:
        return {'message': 'Missing data'}, 400

    title = data.get('title')
    genre = data.get('genre')
    release_date = data.get('release_date')
    year = data.get('year')
    description = data.get('description')

    try:
        if release_date:
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
        year = int(year) if year is not None else None
    except (TypeError, ValueError):
        return {'error': 'Release date must be YYYY-MM-DD and year must be a valid number'}, 400

    movie = {
        'title': title,
        'genre': genre,
        'release_date': release_date,    
        'year': year,
        'description': description
    }

    if not all([movie['title'], movie['genre'], movie['release_date'], movie['year'], movie['description']]):
        return {'message': 'All fields are required'}, 400

    result = movies_collection.insert_one(movie)
    return {'message': 'Movie added successfully', 'id': str(result.inserted_id)}, 201


# Get all movies
def get_all_movies_controller():
    movies = list(movies_collection.find())
    return [serialize_movie(movie) for movie in movies], 200


# Get a movie by ID
def get_movie_controller(movie_id, data=None):
    if not ObjectId.is_valid(movie_id):
        return {'error': 'Invalid movie ID'}, 400

    movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return {'error': 'Movie not found'}, 404

    return {'movie': serialize_movie(movie)}, 200


# Update a movie
def update_movie_controller(movie_id, data):
    if not ObjectId.is_valid(movie_id):
        return {'error': 'Invalid movie ID'}, 400

    if not data:
        return {'error': 'Missing data'}, 400

    title = data.get('title')
    genre = data.get('genre')
    release_date = data.get('release_date')
    year = data.get('year')
    description = data.get('description')

    if not all([title, genre, release_date, year, description]):
        return {'error': 'All fields are required'}, 400

    try:
        if isinstance(release_date, str):
            release_date = datetime.strptime(release_date, '%Y-%m-%d')
        year = int(year)
    except (TypeError, ValueError):
        return {'error': 'Year must be a valid number and release date must be YYYY-MM-DD'}, 400

    result = movies_collection.update_one(
        {'_id': ObjectId(movie_id)},
        {'$set': {
            'title': title,
            'genre': genre,
            'release_date': release_date,
            'year': year,
            'description': description
        }}
    )
    if result.matched_count == 0:
        return {'error': 'Movie not found'}, 404
    return {'message': 'Movie updated successfully'}, 200


# Delete a movie
def delete_movie_controller(movie_id):
    if not ObjectId.is_valid(movie_id):
        return {'error': 'Invalid movie ID'}, 400

    result = movies_collection.delete_one({'_id': ObjectId(movie_id)})
    if result.deleted_count == 0:
        return {'error': 'Movie not found'}, 404

    reviews_collection.delete_many({'movie_id': ObjectId(movie_id)})
    return {'message': 'Movie deleted successfully'}, 200


# Get top-rated movies
def get_top_rated_movies_controller():
    movies = list(movies_collection.find())
    ranked_movies = []

    for movie in movies:
        reviews = list(reviews_collection.find({'movie_id': movie['_id']}))
        if reviews:
            avg_rating = sum(float(review.get('rating', 0)) for review in reviews) / len(reviews)
        else:
            avg_rating = 0
        ranked_movies.append({
            'movie_id': str(movie['_id']),
            'title': movie.get('title'),
            'average_rating': round(avg_rating, 2)
        })

    ranked_movies.sort(key=lambda item: item['average_rating'], reverse=True)
    return {'top_rated_movies': ranked_movies[:10]}, 200