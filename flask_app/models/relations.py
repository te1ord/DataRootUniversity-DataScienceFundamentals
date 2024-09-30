from core import db
from sqlalchemy import Table, Column, Integer, ForeignKey

# Table name -> 'association'
# Columns: 'actor_id' -> db.Integer, db.ForeignKey -> 'actors.id', primary_key = True
#          'movie_id' -> db.Integer, db.ForeignKey -> 'movies.id', primary_key = True
association = Table('association', db.metadata,
                    Column('actor_id', ForeignKey('actors.id'), primary_key=True),
                    Column('movie_id', ForeignKey('movies.id'), primary_key=True))