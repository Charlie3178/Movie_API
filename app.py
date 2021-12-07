from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

#
# Database Setup
#
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String,nullable=False,unique=True)
    genre = db.Column(db.String,nullable=False)
    mpaa_rating = db.Column(db.String)
    poster_img = db.Column(db.String,unique=True)
    all_reviews = db.relationship('Review', backref='movie', cascade='all,delete,delete-orphan')
#
# column definitions
#
    def __init__(self, title, genre, mpaa_rating, poster_img, all_reviews):
        self.title = title
        self.genre = genre
        self.mpss_rating = mpaa_rating
        self.poster_img = poster_img
        self.all_reviews = all_reviews

class Review(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    star_rating = db.column(db.Float,nullable=False)
    review_text = db.Column(db.Text,length=280)
    movie_id = db.column(db.Integer, db.ForeignKey('movie.id'),nullable=False)

    def __init__(self, star_rating, review_text,movie_id):
        self.star_rating = star_rating
        self.review_text = review_text
        self.movie_id = movie_id
#
# Schema Setup
#

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('id','star_rating','review_text','movie_id')

review_schema = ReviewSchema()
multi_review_shcema = 


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id','title','genre','mpaa-rating','poster_img')
    all_reviews = ma.Nested(multi

movie_schema = MovieSchema()
multi_moveie_schema = MovieSchema(many=True)

#
# Post Endpoint
#
@app.route('/movie/add', methods=["POST"])
def add_movie():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    
    post_data = request.get_json()
    title = post_data.get('title')
    genre = post_data.get('genre')
    mpaa_rating = post_data.get('mpaa_rating')
    poster_img = post_data.get('poster_img')

    if title == None:
        return jsonify('Error: Title must be provided')
    if genre == None:
        return jsonify('Error: Genre must be provided')

    new_record = Movie(title, genre, mpaa_rating, poster_img)
    db.session.add(new_record)
    db.session.commit()

    return jsonify(movie_schema.dump(new_record))

# Endpoint for a get-all request
@app.route('/movies/get', methods=['GET'])
def get_all_movies():
    all_records = db.session.query(Movie).all()
    return jsonify(multi_moveie_schema.dump(all_records))

# Endpoint for a get1 request
@app.route('/movie/get/<id>', methods=['GET'])
def get_movie_by_id(id):
    one_movie = db.session.query(Movie).filter(Movie.id==id).first()
    return jsonify(movie_schema.dump(one_movie))

@app.route('/movie/update/<id>',methods=['PUT'])
def update_movie_by_id(id):
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')

    put_data = request.get_json()
    title = put_data.get('title')
    genre = put_data.get('genre')
    mpaa_rating = put_data.get('mpaa_rating')
    poster_img = put_data.get('poster_img')

    movie_to_update = db.session.query(Movie).filter(Movie.id==id).first()


    if title != None:
        movie_to_update.title = title
    if genre != None:
        movie_to_update.genre = genre
    if mpaa_rating != None:
        movie_to_update.mpaa_rating = mpaa_rating
    if poster_img != None:
        movie_to_update.poster_img = poster_img

    db.session.commit()

    return jsonify(movie_schema.dump(movie_to_update))

# Endpoint to delete
@app.route('/movie/delete/<id>', methods=['DELETE'])
def delete_movie_by_id(id):
    movie_to_delete = db.session.query(Movie).filter(Movie.id==id).first()
    db.session.delete(movie_to_delete)
    db.session.commit()
    return jsonify('Movie Successfully Deleted')

























































if __name__ == "__main__":
    app.run(debug=True)