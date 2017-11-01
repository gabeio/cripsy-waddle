import json
from flask import Blueprint
from flask import request
from curlydollop.database import User, db
from sqlalchemy import exc

users = Blueprint('users', __name__, template_folder='templates')

# CREATE
@users.route('', methods=['POST'])
def create():
    params = {}
    if 'title' in request.form.keys():
        params['title'] = request.form['title']
    if 'uri' in request.form.keys():
        params['uri'] = request.form['uri']
    u = User(**params)
    try:
        db.session.add(u)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'create'}, separators=(',',':')), 201

# RETRIEVE
@users.route('/<id>', methods=['GET'])
def all():
    u = []
    q = User.query.order_by('id').all()
    for user in q:
        u.append(user.obj())
    return json.dumps(s, separators=(',',':')), 200

# id (required)
@users.route('/<id>', methods=['GET'])
def one(id):
    u = User.query.get(id)
    return json.dumps(u.obj(), separators=(',',':')), 200



# UPDATE
# id (required)
@users.route('/<id>', methods=['PUT'])
def update(id):
    u = User.query.get(id)
    if 'title' in request.form.keys():
        u.title = request.form['title']
    if 'uri' in request.form.keys():
        u.uri = request.form['uri']
    try:
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'update'}, separators=(',',':')), 200

# DELETE
# id (required)
@users.route('/<id>', methods=['DELETE'])
def delete(id):
    u = User.query.get(id)
    try:
        db.session.delete(u)
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'delete'}, separators=(',',':')), 200
