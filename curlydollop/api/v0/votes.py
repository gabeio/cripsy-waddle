import json
from flask import Blueprint
from flask import request
from curlydollop.database import Song, db
from sqlalchemy import exc

votes = Blueprint('votes', __name__, template_folder='templates')

# Vote
# id (required)
@votes.route('/<id>', methods=['PUT'])
def vote(id):
    s = Song.query.get(id)
    s.votes += 1
    try:
        db.session.flush()
        db.session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        return "FAILED", 500
    return json.dumps({'action':'vote'}, separators=(',',':')), 200
