# project/tests/test_scores_model.py

from project.tests.base import BaseTestCase
from project.tests.utils import add_score


class TestScoreModel(BaseTestCase):

    def test_add_score(self):
        score = add_score()
        self.assertTrue(score.id)
        self.assertTrue(score.user_id)
        self.assertTrue(score.exercise_id)
        self.assertTrue(score.correct)
        
