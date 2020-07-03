from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

from flask_migrate import Migrate


#database_path = os.environ['DATABASE_URL']

database_path = "postgres://{}:{}@{}/{}".format('postgres', '00000', 'localhost:5432', 'casting_2')
#postgres://amgyajfqxqjwee:698ed6853d9e679533d02c1c10f60fdcf74def54d84ac8c38dec20188e648b07@ec2-35-169-254-43.compute-1.amazonaws.com:5432/d9nsgsemr11q5u

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
   ## migrate = Migrate(app,db)

'''
Movies
have title and release date
'''

class Movies(db.Model):
    __tablename__ = 'movies'
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(80), nullable=False)
    release_date = Column(db.Date, nullable = False)


    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
          'id': self.id,
          'title': self.title,
          'release_date': self.release_date}


'''
Actors
have name, age, gender
'''

class Actors(db.Model):
    __tablename__ = 'actors'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(80), nullable=False)
    age = Column(db.Integer, nullable = False)
    gender = Column(db.String(10),nullable = False)


    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender


    def insert(self):
        db.session.add(self)
        db.session.commit()
  
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def format(self):
        return {
          'id': self.id,
          'name': self.name,
          'age': self.age,
          'gender': self.gender}



'''
many_to_many
relationship
'''

actor_roles = db.Table('actor_roles',
                   Column('actors_id', db.Integer, db.ForeignKey('actors.id'), primary_key = True),
                   Column('movies_id', db.Integer, db.ForeignKey('movies.id'), primary_key = True))


