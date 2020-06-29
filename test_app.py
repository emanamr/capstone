import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movies, Actors


class CapstoneTestCase(unittest.TestCase):
    """This class represents capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_2"
        self.database_path = "postgres://{}:{}@{}/{}".format('postgres', '00000', 'localhost:5432',  self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

##========================= test get movies ========================##    

    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_404_get_movies(self):

        response = self.client().get('/movies?page=900000')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')

##========================== test get actors =========================##

    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])



    def test_404_get_actors(self):

        response = self.client().get('/actors?page=900000')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')


##=========================== test delete movies ========================##

    def test_delete_movies(self):
        self.movie_id = movie_id

        response = self.client().delete('/movies/'+ str(movie_id))

        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id== movie_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)
        self.assertEqual(movie, None)


    def test_404_delete_movies(self):

        response = self.client().delete('/movies/99999999')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')



##=========================== test delete actors ========================##

    def test_delete_actors(self):

        self.actor_id = actor_id

        response = self.client().delete('/actors/'+ str(actor_id))

        data = json.loads(response.data)
        actor = Actors.query.filter(Actors.id== movie_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(actor, None)


    def test_404_delete_actors(self):

        response = self.client().delete('/actors/99999999')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')


##======================== test post movies ======================##


    def test_post_movies(self):
        movie = {
            'title': 'the game',
            'release_date': '2003-12-6'
            }
        response = self.client().post('/movies/create', json=movie)
        json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_post_movies(self):
        response = self.client().post('/movies/create')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


##======================= test post actors =========================##

    def test_post_actors(self):
        actor = {
            'name': 'roqqaya',
            'age': 22,
            'gender': 'female'
        }
        response = self.client().post('/actors/create', json=actor)

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_422_post_actors(self):
        response = self.client().post('/actors/create')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


##===================== test patch movies ============================##

    def test_patch_movies(self, movie_id):
        self.movie_id = movie_id

        response = self.client().patch('/movies/'+ str(movie_id)+'/edit')

        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id== movie_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

       

    def test_404_patch_movies(self):
        response = self.client().patch('/movies/9999999999999/edit')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')



##====================== test patch actors ============================##

    def test_patch_actors(self):
        self.actor_id = actor_id

        response = self.client().patch('/actors/'+ str(actor_id)+'/edit')

        data = json.loads(response.data)
        actor = Actors.query.filter(Actors.id== actor_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

       

    def test_404_patch_actors(self):
        response = self.client().patch('/actors/9999999999999/edit')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
