
import os
from flask import (Flask, request, abort, jsonify)
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import (Movies, Actors, setup_db)

###============================== start my app ================================###
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

###============================= get movies ===================================###

    @app.route('/movies' , methods=['GET'])
    def get_movies():

        movies_list = Movies.query.all()
        if len(movies_list) == 0:
            abort(404)
        movies = [movie.format() for movie in movies_list]
        return jsonify({
            "success": True, 
            "movies": movies
            }),200


###============================================================================###

###============================= get actors ===================================###

    @app.route('/actors' , methods=['GET'])
    def get_actors():

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


    @app.route('/movies/create' , methods = ['POST'])
    #@requires_auth('post:movies')
    def creat_movie():
        form = request.get_json()
        title =form.get('title')
        release_date = form.get('release_date')
        try:

            movie = Movies(title = title, release_date = release_date)
            movie.insert()
            movie.format()
            return jsonify({
                    "success": True,
                    "movies": movie
                    }), 200
        except:
            abort(404)

###=============================================================================###

###=============================== post actor ==================================###


    @app.route('/actors/create' , methods = ['POST'])
    #@requires_auth('post:actors')
    def creat_actor():
        form = request.get_json()
        name =form.get('name')
        age = form.get('age')
        gender = form.get('gender')
        try:

            actor = Actors(name = name, age = age, gender = gender)
            actor.insert()
            actor.format()
            return jsonify({
                    "success": True,
                    "actors": actor
                    }), 200
        except:
            abort(404)

###=============================================================================###

###============================ patch movies ===================================###

    @app.route('/movies/<int:movie_id>/edit' , methods = ['PATCH'])
    #@requires_auth('patch:movies')
    def patch_movie(movie_id):
        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            try:
                form = request.get_json()
                movie.title = form.get('title')
                movie.release_date =form.get('release_date')
                movie.update()
                movie.format()
                return jsonify({
                    "success": True,
                    "movies": movie
                    }) ,200
            except:
                abort(422)
        except:
            abort(422)

###=============================================================================###


###============================ patch actors ===================================###

    @app.route('/actors/<int:actor_id>/edit' , methods = ['PATCH'])
    #@requires_auth('patch:actors')
    def patch_actor(actor_id):
        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            try:
                form = request.get_json()
                actor.name = form.get('name')
                actor.age =form.get('age')
                actor.update()
                actor.format()
                return jsonify({
                    "success": True,
                    "actors": actor
                    }) ,200
            except:
                abort(422)

        except:
            abort(422)

###=============================================================================###


###========================== delete movies ====================================###


    @app.route('/movies/<int:movie_id>' , methods = ['DELETE'])
    #@requires_auth('delete:movies')
    def delet_movie(movie_id):

        try:
            movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
            if movie is None:
                abort(404)
            try:
                movie.delete()
                return jsonify({
                    "success": True,
                    "delete": movie_id
                    }) ,200
            except:
                abort(422)
        except:
            abort(422)

###===============================================================================###

###========================== delete actors ====================================###


    @app.route('/actors/<int:actor_id>' , methods = ['DELETE'])
    #@requires_auth('delete:movies')
    def delet_actor(actor_id):

        try:
            actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
            if actor is None:
                abort(404)
            try:
                actor.delete()
                return jsonify({
                    "success": True,
                    "delete": actor_id
                    }) ,200
            except:
                abort(422)
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


         #@app.errorhandler(AuthError)
        #def authentification_failed(ex):
        #return jsonify({
            #"success": False,
            #"error": ex.status_code,
            #"message": get_error_message(ex.error, "authentification fails")
                      ## # }), ex.status_code

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