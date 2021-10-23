from dataclasses import dataclass

import requests
from flask import Flask, jsonify, abort
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

from producer import publish

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://admin:p4ssw0rd@db/terror_watch_main"
CORS(app)

db = SQLAlchemy(app)


@dataclass
class Post(db.Model):
    id: int
    title: str
    image: str

    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


@dataclass()
class PostUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'post_id', name='user_post_unique')


@app.route('/api/posts')
def index():
    return jsonify(Post.query.all())


@app.route('/api/posts/<int:id>/vote', methods=['POST'])
def vote(id):
    req = requests.get('http://docker.for.mac.localhost:8000/api/user')
    json = req.json()

    try:
        post_user = PostUser(user_id=json['id'], post_id=id)
        db.session.add(post_user)
        db.session.commit()

        publish('post voted for', id)
    except Exception as e:
        print(e)
        abort(400, 'You already voted for this post')

    return jsonify({
        'message': 'success'
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
