from flask import jsonify, make_response

from models.actor import Actor
from models.movie import Movie
from settings.constants import MOVIE_FIELDS
from . parse_request import get_request_data


def get_all_movies():
    """
    Get list of all records
    """
    all_movies = Movie.query.all()
    movies = []
    for movie in all_movies:
        mov = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
        movies.append(mov)
    return make_response(jsonify(movies), 200)


def get_movie_by_id():
    """
    Get record by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)

        obj = Movie.query.filter_by(id=row_id).first()
        try:
            movie = {k: v for k, v in obj.__dict__.items() if k in MOVIE_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(movie), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def add_movie():
    """
    Add new movie
    """
    data = get_request_data()
    if all(item in MOVIE_FIELDS for item in data.keys()):  # Inputted fields should exist
        if len(data.keys()) != len(MOVIE_FIELDS) - 1:  # All required fields should be specified
            return make_response(jsonify(error='All required fields should be specified'), 400)
        if 'year' in data.keys():
            try:
                year = int(data['year'])
                if year > 2021:
                    err = 'Wrong year format'
                    return make_response(jsonify(error=err), 400)
            except:
                err = 'Year must be integer'
                return make_response(jsonify(error=err), 400)
            # use this for 200 response code
            new_record = Movie.create(**data)
            new_movie = {k: v for k, v in new_record.__dict__.items() if k in MOVIE_FIELDS}
            return make_response(jsonify(new_movie), 200)
        else:
            err = 'Inputted fields should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Inputted fields should exist'
        return make_response(jsonify(error=err), 400)


def update_movie():
    """
    Update movie record by id
    """
    data = get_request_data()
    if all(item in MOVIE_FIELDS for item in data.keys()):  # Inputted fields should exist
        # use this for 200 response code
        if 'id' in data.keys():
            try:
                row_id = int(data['id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)
            try:
                if 'year' in data.keys():
                    try:
                        year = int(data['year'])
                        if year > 2021:
                            err = 'Wrong year format'
                            return make_response(jsonify(error=err), 400)
                    except:
                        err = 'Year must be integer'
                        return make_response(jsonify(error=err), 400)
                    # use this for 200 response code
                    upd_record = Movie.update(row_id, **data)
                    upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
                    return make_response(jsonify(upd_movie), 200)
                else:
                    upd_record = Movie.update(row_id, **data)
                    upd_movie = {k: v for k, v in upd_record.__dict__.items() if k in MOVIE_FIELDS}
                    return make_response(jsonify(upd_movie), 200)
            except:
                err = 'Such movie id record should exist'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Inputted fields should exist'
        return make_response(jsonify(error=err), 400)


def delete_movie():
    """
    Delete movie by id
    """
    data = get_request_data()
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            delete_record = Movie.delete(row_id)
            # use this for 200 response code
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        except:
            err = 'Such movie id record should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def movie_add_relation():
    """
    Add actor to movie's cast
    """
    data = get_request_data()
    if 'id' in data.keys() and 'relation_id' in data.keys():
        try:
            movie_id = int(data['id'])
            actor_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            # use this for 200 response code
            actor = Actor.query.filter_by(id=actor_id).first()
            movie = Movie.add_relation(movie_id, actor)  # add relation here
            rel_movie = {k: v for k, v in actor.__dict__.items() if k in MOVIE_FIELDS}
            rel_movie['cast'] = str(movie.cast)
            return make_response(jsonify(rel_movie), 200)
        except:
            err = 'Such actor or movie id record should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)


def movie_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            movie_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            # use this for 200 response code
            movie = Movie.clear_relations(movie_id)  # clear relations here
            rel_actor = {k: v for k, v in movie.__dict__.items() if k in MOVIE_FIELDS}
            rel_actor['cast'] = str(movie.cast)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Such movie id record should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###