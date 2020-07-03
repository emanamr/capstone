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


        self.PRODUCER_TOKEN='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpORnNpeFQwNU11bXB3UmVUQ3pVUyJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja3Rlc3QuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmJjNTg4YjA3ZTkwMDAxOWU1MWE2OCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTM4MDE4OTUsImV4cCI6MTU5MzgwOTA5NSwiYXpwIjoid1BHNXhXRDN0MGFrMnBEWnFZQzRUQ2Y4RVg5Y1dPcDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.y6pbc4wbQfRNgTeEYltH0jG7ALXabirH2tv9rvW3JSDDhVUkEiFHVcHYh_k2uJvjwbwODpovIHgbJqkpNQ8t2Y3TT4Xe0yWE069lRFoXMlmrOFys1huljZvTw_-RGNTCZGjMBWG6fesPYsaWwq5F6vyuWXALOUCebzBIOSUBkJPJi7ZgNv2WFrb7zzXoReAP1f-_Aab7MbSuhnhhAtBcKbjodu9uz9PuC1rDJd344bJe-a9Rbbjy7Nlm47__Xxj92jgiimcAhRV_ZA4yQJxe6AgEkXvgY4fffFKi8q93FGbk0BDRAUGnwc-8ZRn08fQe7zfRJsJ0bs67Uo8laFRnTw'
        self.DIRECTOR_TOKEN='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImpORnNpeFQwNU11bXB3UmVUQ3pVUyJ9.eyJpc3MiOiJodHRwczovL2Z1bGxzdGFja3Rlc3QuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZmJjNTg4YjA3ZTkwMDAxOWU1MWE2OCIsImF1ZCI6ImNhc3RpbmciLCJpYXQiOjE1OTM4MDEzMDUsImV4cCI6MTU5MzgwODUwNSwiYXpwIjoid1BHNXhXRDN0MGFrMnBEWnFZQzRUQ2Y4RVg5Y1dPcDUiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.zWOAJE1aHb2Oc8l-ETBSWkPF0CcpYPief9XjVUhHhqptRFNVc4yfpYZoxtC86b323Jn8hh2j6eptz-_sdxGhy-2BKcvYyuX_4xuQ6SgdrMnWtN8BFQ-weyBhJ0H3VmEhBgpqww7zWCO5lMK9fdtRdJbeJnWGJb2m4iiN9U_EgXtm175haxFA-8Q8IM0evTLykrbnrU8JFEld_tEvGfR3kU5h2pFWF8k1f70GZwpUtkbyefEpKJ1mm4X0gcNGJbr5vWNtUdGjkWFeTcdS_0b0SnkvULG2PhD5RJbUzWz3bci9g6QWQFrSz2vFdNciFiPo3p98Wr8bSTFiB6TF9nEe_Q'
        self.post_movie={
            'title': 'The Dark Knight',
            'release_date': '2011-08-22'
        }

        self.post_movie_error={
            'title': 'The Dark Knight Rises'
        }

        self.post_actor = {
            'name': 'roqqaya',
            'age': 22,
            'gender': 'female'
        }

        self.post_actor_error={
            'name':'hamza'
            }

        self.patch_movie={
            'title':'dark',
            'release_date':'2010-04-23'
        }

        self.patch_actor={
            'name': 'hamza',
            'age': 42,
            'gender': 'male'
            }
        
        self.executive_producer_header={
            'Content-Type': 'application/json',
            'Authorization': self.PRODUCER_TOKEN
        }

        self.casting_director_header={
            'Content-Type': 'application/json',
            'Authorization': self.DIRECTOR_TOKEN
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
        response =self.client().get('/movies', headers=self.casting_director_header)
        data=json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])


    def test_404_get_movies(self):
       
        response = self.client().get('/movies', headers=self.casting_director_header)

        data = json.loads(response.data.decode('utf-8'))
        if data is None:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['error'], 404)
            self.assertEqual(data['message'], 'Not found')

##========================== test get actors =========================##

    def test_get_actors(self):
        res=self.client().get('/actors', headers=self.casting_director_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])



    def test_404_get_actors(self):
        
        response = self.client().get('/actors', headers=self.casting_director_header)

        data = json.loads(response.data)
        if data is None:
            self.assertEqual(response.status_code, 404)
            self.assertEqual(data['success'], False)
            self.assertEqual(data['error'], 404)
            self.assertEqual(data['message'], 'Not found')


##=========================== test delete movies ========================##

    def test_delete_movies(self):
        
        response = self.client().delete('/movies/30', headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))
        
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 30)
        


    def test_422_delete_movies(self):

        response = self.client().delete('/movies/99999999', headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')



##=========================== test delete actors ========================##

    def test_delete_actors(self):
        
        response = self.client().delete('/actors/30', headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))
        

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 30)
        


    def test_422_delete_actors(self):

        response = self.client().delete('/actors/99999999', headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


##======================== test post movies ======================##

    def test_post_movie(self):
        res=self.client().post('/movies', json=self.post_movie, headers=self.executive_producer_header)
        data=json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post_movie_error(self):
        res=self.client().post('/movies', json=self.post_movie_error, headers=self.executive_producer_header)
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
        
        response = self.client().post('/actors', json=self.post_actor, headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)


    def test_404_post_actors(self):
        
        response = self.client().post('/actors', json=self.post_actor_error, headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')


##===================== test patch movies ============================##

    def test_patch_movies(self):
        

        response = self.client().patch('/movies/19', json=self.patch_movie , headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

       

    def test_404_patch_movies(self):
        response = self.client().patch('/movies/9999999999999' , json=self.patch_movie , headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Not found')



##====================== test patch actors ============================##

    def test_patch_actors(self):
       

        response = self.client().patch('/actors/7', json=self.patch_actor , headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

       

    def test_422_patch_actors(self):
        response = self.client().patch('/actors/999', json=self.patch_actor , headers=self.executive_producer_header)

        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 422)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
