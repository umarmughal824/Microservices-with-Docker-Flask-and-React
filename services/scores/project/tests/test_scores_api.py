# services/scores/project/tests/test_scores_api.py


import json
import unittest

from project.tests.base import BaseTestCase
from project.tests.utils import add_score


class TestScoresService(BaseTestCase):
    """Tests for the Scores Service."""

    def test_score_ping(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/scores/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_all_scores(self):
        """Ensure get all scores behaves correctly."""
        add_score(1, 1, True)
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

    def test_single_score_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.get(
            '/scores/user/123',
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_single_score(self):
        """Ensure get single score by user_id behaves correctly."""
        score = add_score(user_id=998877, 
                          exercise_id=2, 
                          correct=True)
        with self.client:
            response = self.client.get(
                f'/scores/user/{score.exercise_id}',
                headers={'Authorization': 'Bearer test'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(998877, data['data']['user_id'])
            self.assertEqual(2, data['data']['exercise_id'])
            self.assertEqual(True, data['data']['correct'])
            self.assertEqual('success', data['status'])

    def test_single_score_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get(
                '/scores/user/qq',
                headers={'Authorization': 'Bearer test'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Score does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_sngle_score_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get(
                '/scores/user/123',
                headers={'Authorization': 'Bearer test'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('Score does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_user_scores_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.get(
            '/scores/user',
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])

    def test_user_scores(self):
        """Ensure get scores by user_id behaves correctly."""
        add_score(user_id=998877, 
                  exercise_id=2, 
                  correct=True)
        
        score = add_score(user_id=998877, 
                          exercise_id=3, 
                          correct=False)
        with self.client:
            response = self.client.get(
                '/scores/user',
                headers={'Authorization': 'Bearer test'}
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(998877, data['data']['scores'][0]['user_id'])
            self.assertEqual(2, data['data']['scores'][0]['exercise_id'])
            self.assertEqual(True, data['data']['scores'][0]['correct'])
            self.assertEqual(998877, data['data']['scores'][1]['user_id'])
            self.assertEqual(3, data['data']['scores'][1]['exercise_id'])
            self.assertEqual(False, data['data']['scores'][1]['correct'])
            self.assertEqual('success', data['status'])

    def test_update_score(self):
        """Ensure an existing score can be updated in the database."""
        score = add_score(998877, 65479, True)
        with self.client:
            response = self.client.put(
                f'/scores/{score.exercise_id}',
                data=json.dumps({'correct': False}),
                content_type='application/json',
                headers=({'Authorization': 'Bearer test'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('Score was updated!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_score_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.put(
                '/scores/7',
                data=json.dumps({}),
                content_type='application/json',
                headers=({'Authorization': 'Bearer test'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_update_score_invalid_exercise_id(self):
        """Should create the score if it doesn't exist."""
        add_score(998877, 65479, True)
        with self.client:
            response = self.client.put(
                '/scores/9',
                data=json.dumps({'correct': False}),
                content_type='application/json',
                headers=({'Authorization': 'Bearer test'})
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('New score was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_update_score_no_header(self):
        """Ensure error is thrown if 'Authorization' header is empty."""
        response = self.client.put(
            '/scores/9',
            data=json.dumps({'correct': False}),
            content_type='application/json'
        )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 403)
        self.assertIn('Provide a valid auth token.', data['message'])
        self.assertIn('error', data['status'])


if __name__ == '__main__':
    unittest.main()
