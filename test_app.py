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


        self.PRODUCER_TOKEN='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpORnNpeFQwNU11bXB3UmVUQ3pVUyJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja3Rlc3QuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmJjNTg4YjA3ZTkwMDAxOWU1MWE2OCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTM1NzI1MzYsImV4cCI6MTU5MzU3OTczNiwiYXpwIjoid1BHNXhXRDN0MGFrMnBEWnFZQzRUQ2Y4RVg5Y1dPcDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q7YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.2Bmy_ZYde0dGfVpiiRsycLoeCg6XFkY439eJZdgIe_AbLAS4MkBnM2EFTAv6JhA2m6SD7tUZM1vqcyVJMGglwjpkoaFzv5fsKSCxfyZ6ItavQn5sCumTbpt_IXNwu_X5iPz3lDGj3v-9h8x4-X-ncN34h4Wt16W8jC64_aE7Y3pFbJD6U_kHmILtwqS_NP2Yvt9DFlo9eqNYwC51gIQ8AtenB7XMuHGSn3xvjB3b-23D0hA5kEGgq9RJZ3dkcfwW8HlmaS9f08o6OCuoMYQmV1N8A__mp9MoIX6PITdXo7ypadH6qOuW5DMNVqoUcYMMZPUcuK-fhFBMuLlgKlIwoQ'
        
        self.post_movie={
            'title': 'The Dark Knight',
            'release_date': '2011-08-22'
        }

        self.post_movie_error={
            'title': 'The Dark Knight Rises'
        }
        
        self.executive_producer_header={
            'Content-Type': 'application/json',
            'Authorization': self.PRODUCER_TOKEN
        }
        
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
        Movies.query.delete()
        response = self.client().get('/movies')

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
        Actors.query.delete()
        response = self.client().get('/actors')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')


##=========================== test delete movies ========================##

    def test_delete_movies(self):
        
        response = self.client().delete('/movies/3')

        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id== 3).one_or_none()
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 3)
        self.assertEqual(movie, None)


    def test_422_delete_movies(self):

        response = self.client().delete('/movies/99999999')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')



##=========================== test delete actors ========================##

    def test_delete_actors(self):
        actor_id=1
        response = self.client().delete('/actors/1')

        data = json.loads(response.data)
        actor = Actors.query.filter(Actors.id== actor_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)
        self.assertEqual(actor, None)


    def test_422_delete_actors(self):

        response = self.client().delete('/actors/99999999')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


##======================== test post movies ======================##

    def test_post_movie(self):
        res=self.client().post('/movies/create', json=self.post_movie, headers=self.executive_producer_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post_movie_error(self):
        res=self.client().post('/movies/create', json=self.post_movie_error, headers=self.executive_producer_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')




    '''
    def test_post_movies(self):
        movie = {
            'title': 'the game',
            'release_date': '2003-12-6'
            }
        response = self.client().post('/movies/create', json=movie)
        json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_404_post_movies(self):
        response = self.client().post('/movies/create')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')

    '''
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

    def test_patch_movies(self):
        movie_id = 2

        response = self.client().patch('/movies/'+ str(movie_id)+'/edit')

        data = json.loads(response.data)
        movie = Movies.query.filter(Movies.id== movie_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

       

    def test_422_patch_movies(self):
        response = self.client().patch('/movies/9999999999999/edit')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')



##====================== test patch actors ============================##

    def test_patch_actors(self):
        actor_id = 1

        response = self.client().patch('/actors/'+ str(actor_id)+'/edit')

        data = json.loads(response.data)
        actor = Actors.query.filter(Actors.id== actor_id).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

       

    def test_422_patch_actors(self):
        response = self.client().patch('/actors/9999999999999/edit')

        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
