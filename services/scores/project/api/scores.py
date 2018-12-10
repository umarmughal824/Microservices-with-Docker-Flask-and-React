# services/scores/project/api/scores.py

from sqlalchemy import exc
from flask import Blueprint, jsonify, request

from project import db
from project.api.models import Score
from project.api.utils import authenticate

scores_blueprint = Blueprint('scores', __name__)


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
    if not resp['admin']:
        response_object = {
            'status': 'error',
            'message': 'You do not have permission to do that.'
        }
        return jsonify(response_object), 401

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
