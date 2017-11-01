import json
from flask import Blueprint
from flask import request
from curlydollop.database import Song, db
from sqlalchemy import exc

songs = Blueprint('songs', __name__, template_folder='templates')

# CREATE
@songs.route('', methods=['POST'])
def create():
    params = {}
    if 'title' in request.form.keys():
        params['title'] = request.form['title']
    if 'uri' in request.form.keys():
        params['uri'] = request.form['uri']
    s = Song(**params)
    try:
        db.session.add(s)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'create'}, separators=(',',':')), 201

# RETRIEVE
@songs.route('', methods=['GET'])
def all():
    s = []
    q = Song.query.order_by('id').all()
    for song in q:
        s.append(song.obj())
    return json.dumps(s, separators=(',',':')), 200

# id (required)
@songs.route('/<id>', methods=['GET'])
def one(id):
    s = Song.query.get(id)
    return json.dumps(songs.obj(), separators=(',',':')), 200

# UPDATE
# id (required)
@songs.route('/<id>', methods=['PUT'])
def update(id):
    s = Song.query.get(id)
    if 'title' in request.form.keys():
        s.title = request.form['title']
    if 'uri' in request.form.keys():
        s.uri = request.form['uri']
    try:
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'update'}, separators=(',',':')), 200

# DELETE
# id (required)
@songs.route('/<id>', methods=['DELETE'])
def delete(id):
    s = Song.query.get(id)
    try:
        db.session.delete(s)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'delete'}, separators=(',',':')), 200
