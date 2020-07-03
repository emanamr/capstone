Full Stack Casting Agency API
About
Getting Started
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. The app is used to store Actors to casting and store Movies too.

The casting agency has a Casting Director who has permisiions to post, modify and view actors or movies, they are also allowed to delete actors. There is also a Executive Producer who is not only permitted to to all the same actions the Casting Director is but also allowed to delete movies.

The endpoints and how to send requests to these endpoints for products and items are described in the 'Endpoint Library' section of the README.

All endpoints need to be tested using curl since there is no frontend for the app yet.

Installing Dependencies
Python 3.7
Follow instructions to install the latest version of python for your platform in the python docs

PIP Dependencies
Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:

pip install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.

Key Dependencies
Flask is a lightweight backend microservices framework. Flask is required to handle requests and responses.

SQLAlchemy and Flask-SQLAlchemy are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in ./src/database/models.py. We recommend skimming this code first so you know how to interface with the Drink model.

jose JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

Flask-CORS is the extension we'll use to handle cross origin requests from our frontend server.

Running the server
To run the server, execute:

set FLASK_APP=app
set FLASK_ENV=development
flask run
 
alternatively you could use 

py app.py

The live application can only be used to generate tokens via Auth0, the endpoints may only be tested using curl using the token, since no frontend for the application currently exists.

Data Modeling
models.py
The schema for the database and helper methods to simplify API behaviour are in models.py:

Two tables have been created: Actors and Movies.
The Actor table is used by the roles 'Casting Director' and 'Executive Producer' to add, modify or remove actors from the table.
The Movie table is used by the role 'Exectuive Producer' to add, modify, and remove movies, and by the role 'Casting Director' to add and modify movies from the table.
Both tables have insert, update, delete and format helper function.

Endpoint Library
@app.errorhandler
Decorators were used to format error responses as JSON objects. Custom @requires_auth decorators were used for Authorizations based on roles.

Tokens
A token needs to be passed to each endpoint.The following works for all endpoints: The token can be retrieved by following these steps:

Go to: https://fullstacktest.auth0.com/authorize?audience=casting&response_type=token&client_id=wPG5xWD3t0ak2pDZqYC4TCf8EX9cWOp5&redirect_uri=http://127.0.0.1:5000/ 


GET '/actors'
Fetches a dictionary of actors.
Request Arguments: None.
Return: An object with a single key, success, actors. {
'actors':[ { 'id': 1, 'name': 'Tom Hardy', 'age': 42, 'gender': 'male' }, ... ], 'success': True }

GET '/movies'
Fetches a dictionary of movies.
Request Arguments: None.
Return: An object with a single key, success, movies. { 'movies':[ { 'id': 1, 'title': 'Batman Begins', 'genre': 'Action' }, ... ] 'success': True }

POST '/actors'
Posts a actor to the database.
Request Arguments: Name, Age, Gender.
Return: An object with a singley key, success, movies. {
'actors':[ { 'id': 1, 'name': 'Tom Hardy', 'age': 42, 'gender': 'male' }, ... ], 'success': True }

POSTS '/movies'
Posts a movie to the database.
Request Arguments: Title, Genre.
Return: An object with a single key, success, movies. { 'movies':[ { 'id': 1, 'title': 'Batman Begins', 'genre': 'Action' }, ... ] 'success': True }

PATCH '/actors/int:actor_id'
Patches a actor in the database.
Request Arguments: actor_id, Name, Age, Gender.
Return: An object with a single key, success, actors. {
'actors':[ { 'id': 1, 'name': 'Tom Hardy', 'age': 42, 'gender': 'male' }, ... ], 'success': True }

PATCH '/movies/int:movie_id'
Patches a movie in the database.
Request Arguments: movie_id, Title, Genre.
Return: An object with a single key, success, movies. { 'movies':[ { 'id': 1, 'title': 'Batman Begins', 'genre': 'Action' }, ... ] 'success': True }

DELETE '/actors/int:actor_id'
Deletes a actor from the databse.
Request Arguments: actor_id.
Return: An object with a single key, success, actor_id. { 'deleted_actor': actor_id, 'success': True }

DELETE '/movies/int:movie_id'
Deletes a movie from the database.
Request Arguments: movie_id.
Return: An object with a single key, success, movie_id. { 'deleted_movie': movie_id, 'success': True }

Testing
To run the test_app.py, use:

py test_app.py
The tests include a test for successfull behaviour and a test for error behaviour for each of the ednpoints. All tests demonstrate the use of RBAC, where all the endpoints are tested using the correct authorization.

Third Party Authentication
auth.py
Auth0 is set up and running.

Deployment
The app is hosted live on heroku at the URL: https://emy-casting.herokuapp.com/

Currently no frontend for the app exists, currently it can only be used to authenticate using Auth0 by entering credentials and retrieving a fresh token to use with curl or postman.

Git URL
https://git.heroku.com/emy-casting.git