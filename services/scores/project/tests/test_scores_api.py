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

    def test_add_score(self):
        """Ensure a new score can be added to the database."""
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps({
                    'user_id': 3,
                    'exercise_id': 3,
                    'correct': True,
                }),
                content_type='application/json',
                headers=({'Authorization': 'Bearer test'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('New score was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_score_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps({}),
                content_type='application/json',
                headers=({'Authorization': 'Bearer test'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_score_invalid_json_keys(self):
        """Ensure error is thrown if the JSON object is invalid."""
        with self.client:
            response = self.client.post(
                '/scores',
                data=json.dumps({'user_id': 3}),
                content_type='application/json',
                headers=({'Authorization': 'Bearer test'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_score_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.post(
            '/scores',
            data=json.dumps({
                'user_id': 3,
                'exercise_id': 3,
                'correct': True,
            }),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])


if __name__ == '__main__':
    unittest.main()
