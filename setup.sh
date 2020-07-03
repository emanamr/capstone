

set DATABASE_URL= "postgres://{}:{}@{}/{}".format('postgres', '00000', 'localhost:5432', 'casting_2')


set AUTH0_DOMAIN = 'fullstacktest.auth0.com'
set ALGORITHMS = ['RS256']
set API_AUDIENCE = 'casting'

set FLASK_APP=app.py
set FLASK_ENV=development