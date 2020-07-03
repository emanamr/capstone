
import os
from flask import (Flask, request, abort, jsonify)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (Movies, Actors, setup_db)
import json
from auth import AuthError, requires_auth



###============================== start my app ================================###
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
   # CORS(app)


    CORS(app, resources={'/': {'origins': '*'}})

###==========================  Sets access control ===========================###


    @app.after_request
    def after_request(response):
        
        response.headers.add('Access-Control-Allow-Headers',
                                'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                                'GET,PATCH,POST,DELETE,OPTIONS')
        return response
###============================================================================###


###============================= home page ====================================###


    @app.route('/')
    def index():
        return jsonify({'message': 'Casting API'})



###============================================================================###


###============================= get movies ===================================###

    @app.route('/movies' , methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):

        movies_list = Movies.query.all()
        if len(movies_list) == 0:
            abort(404)
        movies = [movie.format() for movie in movies_list]
        return jsonify({
            "success": True, 
            "movies": movies
            }), (200)


###============================================================================###

###============================= get actors ===================================###

    @app.route('/actors' , methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(token):

        actors_list = Actors.query.all()
        if len(actors_list) == 0:
            abort(404)
        actors = [actor.format() for actor in actors_list]
        return jsonify({
            "success": True, 
            "actors": actors
            }),200


###============================================================================###


###============================== post movies =================================###
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movie(payload):

        form = request.get_json()

        title = form.get('title')
        release_date = form.get('release_date')

        if title is None or release_date is None:
            abort(422)

        try:
            movie = Movies(
                title=title,
                release_date=release_date
            ).insert()

            all_movies = Movies.query.all()
            movies = [movie.format() for movie in all_movies]

            return jsonify({
                'success': True,
                'movies': movies
            }), (200)
        except Exception:
            abort(422)
 

###=============================================================================###

###=============================== post actor ==================================###


    @app.route('/actors' , methods = ['POST'])
    @requires_auth('post:actors')
    def creat_actor(token):

        form = request.get_json()

        name = form.get('name')
        age = form.get('age')
        gender = form.get('gender')

        if name is None or age is None or gender is None:
            abort (404)

        try:

            actor = Actors(name = name, age = age, gender = gender)
            actor.insert()
            all_actors = Actors.query.all()
            actors = [actor.format() for actor in all_actors]
            return jsonify({
                    "success": True,
                    "actors": actors
                    }), 200
        except:
            abort(422)

###=============================================================================###

###============================ patch movies ===================================###
    """
    @app.route('/movies/<int:movie_id>' , methods = ['patch'])
    @requires_auth('patch:movies')
    def patch_movie(token, movie_id):
        form = request.get_json()
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            print(movie)
            if movie is None:
                abort(404)
            try:
                movie.title = form.get('title')
                movie.release_date =form.get('release_date')
                movie.update()
                all_movies = Movies.query.all()
                movies = [movie.format() for movie in all_movies]
                return jsonify({
                    "success": True,
                    "movies": movie
                    }) ,200
            except:
                abort(422)
            
        except:
            abort(422)
   """

###============================ patch movies ===============================###

    @app.route('/movies/<int:movie_id>' , methods = ['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(token, movie_id):
        form = request.get_json()
        movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
        print(movie)
        if movie is None:
            abort(404)
        try:    
            movie.title = form.get('title')
            movie.release_date =form.get('release_date')
            movie.update()
            all_movies = Movies.query.all()
            movies = [movie.format() for movie in all_movies]
            return jsonify({
                "success": True,
                "movies": movies
                }) ,200
        except:
            abort(422)
###============================ patch actors ===================================###

    @app.route('/actors/<int:actor_id>' , methods = ['PATCH'])
    @requires_auth('patch:actors')
    def patch_actor(token, actor_id):
        form = request.get_json()
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(422)
            try:
                actor.name = form.get('name')
                actor.age =form.get('age')
                actor.gender = form.get('gender')
                actor.update()
                all_actors = Actors.query.all()
                actors = [actor.format() for actor in all_actors]
                return jsonify({
                    "success": True,
                    "actors": actors
                    }) ,200
            except:
                abort(422)

        except:
            abort(422)

###=============================================================================###


###========================== delete movies ====================================###


    @app.route('/movies/<int:movie_id>' , methods = ['DELETE'])
    @requires_auth('delete:movies')
    def delet_movie(token, movie_id):

        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            movie.delete()
            return jsonify({
                "success": True,
                "delete": movie_id
                }) ,200
        except:
            abort(422)

###===============================================================================###

###========================== delete actors ====================================###


    @app.route('/actors/<int:actor_id>' , methods = ['DELETE'])
    @requires_auth('delete:actor')
    def delet_actor(token, actor_id):

        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            actor.delete()
            return jsonify({
                "success": True,
                "delete": actor_id
                }) ,200
        except:
            abort(422)

###===============================================================================###

###=============================== Error Handling ================================###


    # reply with json for 404 error
    @app.errorhandler(404)
    def not_found(error):

        return jsonify({

            "success": False,
            "error": 404,
            "message": "Not found"
            }), 404



    # reply with json for 422 error
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
            }), 422



    # reply with json for 500 error
    @app.errorhandler(500)
    def Internal_Server_Error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
            }), 500


    # reply with json for 400 error
    @app.errorhandler(400)
    def Bad_Request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
            }), 400


    # reply with json for 405 error
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "Error": 405,
            "message": 'Method Not allowed'
        }), 405

    @app.errorhandler(AuthError)
    def authentification_failed(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": (ex.error, "authentification fails")         
           }), ex.status_code


###=============================================================================###


    return app


app = create_app()


if __name__ == '__main__':

    app.run(debug=True)

#APP = create_app()

#if __name__ == '__main__':
    #APP.run(host='0.0.0.0', port=8080, debug=True)
    #port = int(os.environ.get("PORT", 5000))
    #App.run(debug=True)