import math
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uri = db.Column(db.String(2000), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    votes = db.Column(db.Integer, default=1, nullable=False)
    submitted = db.Column(db.DateTime, default=datetime.now(), nullable=True)
    # actual score of a song
    def score(self):
        # points/votes
        p = self.votes
        # time in hours since submission
        t = int(((datetime.now() - self.submitted).total_seconds())//3600)
        # gravity
        g = 1.8
        return (p-1)/math.pow((t+2),g)

    def obj(self):
        """Converts a song to an object"""
        doc = {}
        doc['id'] = self.id
        doc['uri'] = self.uri
        doc['title'] = self.title
        doc['votes'] = self.votes
        doc['score'] = self.score()
        doc['ago'] = int(((datetime.now() - self.submitted).total_seconds())//3600)
        return doc

# a table to tell if you have already voted on a song
vote = db.Table('vote',
    db.Column('song_id', db.Integer, db.ForeignKey('song.id'), nullable=False),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
    db.UniqueConstraint('song_id', 'user_id', name='_one_vote_'),
    # __table_args__ = (db.UniqueConstraint('song_id', 'user_id', name='_one_vote_'),)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    passhash = db.Column(db.String(130), nullable=False)
