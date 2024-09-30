from flask import jsonify, make_response

from datetime import datetime as dt
from ast import literal_eval

from models.actor import Actor
from models.movie import Movie
from settings.constants import ACTOR_FIELDS, DATE_FORMAT  # to make response pretty
from . parse_request import get_request_data


def get_all_actors():
    """
    Get list of all records
    """
    all_actors = Actor.query.all()
    actors = []
    for actor in all_actors:
        act = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
        actors.append(act)
    return make_response(jsonify(actors), 200)


def get_actor_by_id():
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

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)

    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)

        obj = Actor.query.filter_by(id=row_id).first()
        try:
            actor = {k: v for k, v in obj.__dict__.items() if k in ACTOR_FIELDS}
        except:
            err = 'Record with such id does not exist'
            return make_response(jsonify(error=err), 400)

        return make_response(jsonify(actor), 200)


def add_actor():
    """
    Add new actor
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if all(item in ACTOR_FIELDS for item in data.keys()):  # Inputted fields should exist
        if len(data.keys()) != len(ACTOR_FIELDS) - 1:  # All required fields should be specified
            return make_response(jsonify(error='All required fields should be specified'), 400)
        if 'date_of_birth' in data.keys():
            date_of_birth = data['date_of_birth']
            try:
                dt.strptime(date_of_birth, DATE_FORMAT).strftime(DATE_FORMAT)
                # use this for 200 response code
                new_record = Actor.create(**data)
                new_actor = {k: v for k, v in new_record.__dict__.items() if k in ACTOR_FIELDS}
                return make_response(jsonify(new_actor), 200)
            except ValueError:
                err = 'Date of birth should be in format DATE_FORMAT'
                return make_response(jsonify(error=err), 400)
    else:
        err = 'Inputted fields should exist'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def update_actor():
    """
    Update actor record by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if all(item in ACTOR_FIELDS for item in data.keys()):  # Inputted fields should exist
        # use this for 200 response code
        if 'id' in data.keys():
            try:
                row_id = int(data['id'])
            except:
                err = 'Id must be integer'
                return make_response(jsonify(error=err), 400)
            try:
                if 'date_of_birth' in data.keys():
                    data_of_birth = data['date_of_birth']
                    if data_of_birth == dt.strptime(data_of_birth, DATE_FORMAT).strftime(DATE_FORMAT):
                        # use this for 200 response code
                        upd_record = Actor.update(row_id, **data)
                        upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
                        return make_response(jsonify(upd_actor), 200)
                else:
                    upd_record = Actor.update(row_id, **data)
                    upd_actor = {k: v for k, v in upd_record.__dict__.items() if k in ACTOR_FIELDS}
                    return make_response(jsonify(upd_actor), 200)
            except:
                err = 'Such actor id record should exist'
                return make_response(jsonify(error=err), 400)
        else:
            err = 'No id specified'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'Inputted fields should exist'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def delete_actor():
    """
    Delete actor by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            row_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            Actor.delete(row_id)
            # use this for 200 response code
            msg = 'Record successfully deleted'
            return make_response(jsonify(message=msg), 200)
        except:
            err = 'Such actor id record should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_add_relation():
    """
    Add a movie to actor's filmography
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys() and 'relation_id' in data.keys():
        try:
            actor_id = int(data['id'])
            movie_id = int(data['relation_id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            # use this for 200 response code
            movie = Movie.query.filter_by(id=movie_id).first()
            actor = Actor.add_relation(actor_id, movie)  # add relation here
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Such actor or movie id record should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###


def actor_clear_relations():
    """
    Clear all relations by id
    """
    data = get_request_data()
    ### YOUR CODE HERE ###
    if 'id' in data.keys():
        try:
            actor_id = int(data['id'])
        except:
            err = 'Id must be integer'
            return make_response(jsonify(error=err), 400)
        try:
            # use this for 200 response code
            actor = Actor.clear_relations(actor_id)  # clear relations here
            rel_actor = {k: v for k, v in actor.__dict__.items() if k in ACTOR_FIELDS}
            rel_actor['filmography'] = str(actor.filmography)
            return make_response(jsonify(rel_actor), 200)
        except:
            err = 'Such actor id record should exist'
            return make_response(jsonify(error=err), 400)
    else:
        err = 'No id specified'
        return make_response(jsonify(error=err), 400)
    ### END CODE HERE ###