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
