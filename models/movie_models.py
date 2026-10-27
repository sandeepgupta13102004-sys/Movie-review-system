from datetime import datetime
from bson import ObjectId
from config import movies_collection, reviews_collection


def serialize(document):
    if document is None:
        return None

    result = dict(document)
    if '_id' in result:
        result['id'] = str(result.pop('_id'))
    if 'movie_id' in result and isinstance(result['movie_id'], ObjectId):
        result['movie_id'] = str(result['movie_id'])
    if 'created_at' in result and isinstance(result['created_at'], datetime):
        result['created_at'] = result['created_at'].isoformat()
    return result


# Movie Model.......
def create_movie(movie_data):
    result = movies_collection.insert_one(movie_data)
    return str(result.inserted_id)


def get_all_movies():
    movies = movies_collection.find().sort('title', 1)
    return [serialize(movie) for movie in movies]


def get_movie_by_id(movie_id):
    if not ObjectId.is_valid(movie_id):
        return None

    movie = movies_collection.find_one({'_id': ObjectId(movie_id)})
    if movie is None:
        return None
    return serialize(movie)


def update_movie(movie_id, movie_data):
    if not ObjectId.is_valid(movie_id):
        return False

    result = movies_collection.update_one({'_id': ObjectId(movie_id)}, {'$set': movie_data})
    return result.matched_count > 0


def delete_movie(movie_id):
    if not ObjectId.is_valid(movie_id):
        return False

    result = movies_collection.delete_one({'_id': ObjectId(movie_id)})
    if result.deleted_count == 0:
        return False

    reviews_collection.delete_many({'movie_id': movie_id})
    return True


# Review Models.....
def create_review(movie_id, review_data):
    if not ObjectId.is_valid(movie_id):
        return None

    review_data['movie_id'] = movie_id
    review_data['comments'] = []

    result = reviews_collection.insert_one(review_data)
    return str(result.inserted_id)


def get_review_by_movie(movie_id):
    if not ObjectId.is_valid(movie_id):
        return []

    reviews = reviews_collection.find({'movie_id': movie_id}).sort('created_at', -1)
    return [serialize(review) for review in reviews]


def get_review_by_id(review_id):
    if not ObjectId.is_valid(review_id):
        return None

    review = reviews_collection.find_one({'_id': ObjectId(review_id)})
    if review is None:
        return None
    return serialize(review)


def update_review(review_id, review_data):
    if not ObjectId.is_valid(review_id):
        return False

    result = reviews_collection.update_one({'_id': ObjectId(review_id)}, {'$set': review_data})
    return result.matched_count > 0


def delete_review(review_id):
    if not ObjectId.is_valid(review_id):
        return False

    result = reviews_collection.delete_one({'_id': ObjectId(review_id)})
    return result.deleted_count > 0


# Comment Models.....
def add_comment(review_id, comment_data):
    if not ObjectId.is_valid(review_id) or not isinstance(comment_data, dict):
        return False
    result = reviews_collection.update_one({'_id': ObjectId(review_id)}, {'$push': {'comments': comment_data}})
    return result.matched_count > 0


def delete_comment(review_id, comment_id):
    if not ObjectId.is_valid(review_id):
        return False
    result = reviews_collection.update_one({'_id': ObjectId(review_id)}, {'$pull': {'comments': {'_id': comment_id}}})
    return result.matched_count > 0 and result.modified_count > 0

