from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://admin:p4ssw0rd@db/terror_watch_main"
CORS(app)

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    title = db.Column(db.String(200))
    image = db.Column(db.String(200))


class PostUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    UniqueConstraint('user_id', 'post_id', name='user_post_unique')


@app.route('/')
def index():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
