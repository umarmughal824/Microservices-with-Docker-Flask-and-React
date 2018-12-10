# services/scores/project/tests/test_scores_api.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_score


class TestScoresService(BaseTestCase):
    """Tests for the Scores Service."""

    def test_all_scores(self):
        """Ensure get all scores behaves correctly."""
        add_score()
        add_score(2, 2, False)
        with self.client:
            response = self.client.get('/scores')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']['scores']), 2)
            self.assertEqual(
                1,
                data['data']['scores'][0]['user_id'])
            self.assertEqual(
                1,
                data['data']['scores'][0]['exercise_id'])
            self.assertEqual(
                True,
                data['data']['scores'][0]['correct'])
            self.assertEqual(
                2,
                data['data']['scores'][1]['user_id'])
            self.assertEqual(
                2,
                data['data']['scores'][1]['exercise_id'])
            self.assertEqual(
                False,
                data['data']['scores'][1]['correct'])
            self.assertIn('success', data['status'])


if __name__ == '__main__':
    unittest.main()
