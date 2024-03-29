from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Movie(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    title = db.Column(db.String,nullable=False,unique=True)
    genre = db.Column(db.String,nullable=False)
    mpaa_rating = db.Column(db.String)
    poster_img = db.Column(db.String,unique=True)
    # all_reviews = db.relationship('Review', backref='movie', cascade='all,delete,delete-orphan')

    def __init__(self, title, genre, mpaa_rating, poster_img):
        self.title = title
        self.genre = genre
        self.mpaa_rating = mpaa_rating
        self.poster_img = poster_img
        
class Review(db.Model):
    id = db.Column(db.Integer,nullable=False,primary_key=True)
    star_rating = db.Column(db.Float,nullable=False)
    review_text = db.Column(db.Text(280))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'),nullable=False)

    def __init__(self, star_rating, review_text,movie_id):
        self.star_rating = star_rating
        self.review_text = review_text
        self.movie_id = movie_id

class ReviewSchema(ma.Schema):
    class Meta:
        fields = ('id','star_rating','review_text','movie_id')

review_schema = ReviewSchema()
multi_review_schema = ReviewSchema(many=True)


class MovieSchema(ma.Schema):
    class Meta:
        fields = ('id','title','genre','mpaa_rating','poster_img', 'all_reviews')
    
movie_schema = MovieSchema()
multi_movie_schema = MovieSchema(many=True)
all_reviews = ma.Nested(multi_review_schema)


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

@app.route('/movies/get', methods=['GET'])
def get_all_movies():
    all_records = db.session.query(Movie).all()
    return jsonify(multi_movie_schema.dump(all_records))

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

    

















        
# class Review(db.Model):
#     id = db.Column(db.Integer,nullable=False,primary_key=True)
#     star_rating = db.Column(db.Float,nullable=False)
#     review_text = db.Column(db.Text(280))
#     movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'),nullable=False)

#     def __init__(self, star_rating, review_text,movie_id):
#         self.star_rating = star_rating
#         self.review_text = review_text
#         self.movie_id = movie_id








# POST Endpoint for a single review
@app.route('/review/add', methods=['POST'])
def add_review():
    if request.content_type != 'application/json':
        return jsonify('Error: Data must be sent as JSON')
    post_data = request.get_json()
    star_rating = post_data.get(star_rating())
    review_text = post_data.get(review_text())
    movie_id = post_data.get(movie_id())

    if title == star_rating:
        return 'You must provide a star rating.'
    if genre == movie_id:
        return 'You must provide a movie ID.'

    new_record = Review(star_rating,review_text,movie_id)
    db.session.add(new_record)
    db.session.commit()



if __name__ == "__main__":
    app.run(debug=True)
