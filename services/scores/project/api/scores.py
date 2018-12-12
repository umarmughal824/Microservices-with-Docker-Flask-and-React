# services/scores/project/api/scores.py

from sqlalchemy import exc, and_
from flask import Blueprint, jsonify, request

from project import db
from project.api.models import Score
from project.api.utils import authenticate

scores_blueprint = Blueprint('scores', __name__)


@scores_blueprint.route('/scores/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@scores_blueprint.route('/scores', methods=['GET'])
def get_all_scores():
    """Get all scores"""
    response_object = {
        'status': 'success',
        'data': {
            'scores': [ex.to_json() for ex in Score.query.all()]
        }
    }
    return jsonify(response_object), 200


@scores_blueprint.route('/scores', methods=['POST'])
@authenticate
def add_score(resp):
    """Add score"""

    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

    user_id = post_data.get('user_id')
    exercise_id = post_data.get('exercise_id')
    correct = post_data.get('correct')

    try:
        db.session.add(Score(
            user_id=user_id,
            exercise_id=exercise_id,
            correct=correct))
        db.session.commit()

        response_object = {
            'status': 'success',
            'message': 'New score was added!'
        }
        return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError) as e:
        db.session().rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400


@scores_blueprint.route('/scores/user/<exercise_id>', methods=['GET'])
@authenticate
def get_single_score(resp, exercise_id):
    """Get single user's score by exercise and user id"""
    response_object = {
        'status': 'fail',
        'message': 'Score does not exist'
    }

    user_id = resp['data']['id']

    try:
        score = Score.query.filter(and_(Score.user_id==int(user_id), 
                                        Score.exercise_id==int(exercise_id))).first()
        if not score:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'user_id': score.user_id,
                    'exercise_id': score.exercise_id,
                    'correct': score.correct
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@scores_blueprint.route('/scores/user', methods=['GET'])
@authenticate
def get_user_scores(resp):
    """Get single user's score by user id"""
    response_object = {
        'status': 'fail',
        'message': 'Score does not exist'
    }

    user_id = resp['data']['id']

    try:
        scores = Score.query.filter_by(user_id=int(user_id))
        if not scores:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'scores': [ex.to_json() for ex in scores]
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@scores_blueprint.route('/scores/<exercise_id>', methods=['PUT'])
@authenticate
def update_score(resp, exercise_id):
    """Update score"""
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400
    correct = post_data.get('correct')
    try:
        score = Score.query.filter_by(
            exercise_id=int(exercise_id),
            user_id=int(resp['data']['id'])
        ).first()
        if score:
            score.correct = correct
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'Score was updated!'
            return jsonify(response_object), 200
        else:
            db.session.add(Score(
                user_id=resp['data']['id'],
                exercise_id=int(exercise_id),
                correct=correct))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = 'New score was added!'
            return jsonify(response_object), 201
    except (exc.IntegrityError, ValueError, TypeError) as e:
        db.session().rollback()
        return jsonify(response_object), 400
