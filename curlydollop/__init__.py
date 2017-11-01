import os
import sys
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from curlydollop.api.v0.songs import songs
from curlydollop.api.v0.users import users
from curlydollop.api.v0.votes import votes
from curlydollop.database import Song, vote, User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
db.init_app(app)

# index
@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(songs, url_prefix='/api/v0/songs')
app.register_blueprint(users, url_prefix='/api/v0/users')
app.register_blueprint(votes, url_prefix='/api/v0/votes')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers["Cache-Control"] = "public, max-age=0"
    return r

if "SETUP_DATABASE" in os.environ.keys():
    with app.app_context():
        db.create_all()
        db.session.commit()
        sys.exit(0) # exit if we are only setting up the database
