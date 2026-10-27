from datetime import datetime, timezone
from bson import ObjectId
from config import movies_collection, reviews_collection


# Add a review and comment
def add_review_controller(movie_id, data):
    if not data:
        return {'message': 'Missing data'}, 400

    if not ObjectId.is_valid(movie_id):
        return {'message': 'Invalid movie ID'}, 400

    movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return {'message': 'Movie not found'}, 404

    username = data.get('username')
    rating = data.get('rating')
    comment = data.get('comment')

    if not all([username, rating, comment]):
        return {'message': 'All fields are required'}, 400

    try:
        rating = float(rating)
    except (TypeError, ValueError):
        return {'message': 'Rating must be a number between 1 and 5'}, 400

    if isinstance(rating, bool) or not 1 <= rating <= 5:
        return {'message': 'Rating must be a number between 1 and 5'}, 400

    if not isinstance(comment, str) or not comment.strip():
        return {'message': 'Comment cannot be empty'}, 400

    review = {
        'movie_id': ObjectId(movie_id),
        'user_name': username.strip(),
        'rating': rating,
        'comment': comment.strip(),
        'created_at': datetime.now(timezone.utc)
    }

    result = reviews_collection.insert_one(review)
    return {
        'message': 'Review added successfully',
        'review_id': str(result.inserted_id),
        'movie_id': movie_id
    }, 201


# Get all reviews for a particular movie
def get_reviews_controller(movie_id):
    if not ObjectId.is_valid(movie_id):
        return {'message': 'Invalid movie ID'}, 400

    movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
    if not movie:
        return {'message': 'Movie not found'}, 404

    reviews = list(reviews_collection.find({'movie_id': ObjectId(movie_id)}).sort('created_at', -1))

    for review in reviews:
        review['id'] = str(review['_id'])
        review['_id'] = str(review['_id'])
        if isinstance(review.get('movie_id'), ObjectId):
            review['movie_id'] = str(review['movie_id'])
        if isinstance(review.get('created_at'), datetime):
            review['created_at'] = review['created_at'].isoformat()

    return {
        'movie_id': str(movie_id),
        'movie_title': movie.get('title'),
        'total_reviews': len(reviews),
        'reviews': reviews
    }, 200