from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    facebook_link = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    seeking_talent = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    # TODO: implement any missing fields, as a database migration using Flask-Migrate # hossam do it =2

    shows = db.relationship('Show', backref='venue_show')

    def __init__(self, name, city, state, address, phone, genres,
                 facebook_link, image_link, seeking_talent, seeking_description):
        self.name = name
        self.city = city
        self.state = state
        self.address = address
        self.phone = phone
        self.genres = genres
        self.facebook_link = facebook_link
        self.image_link = image_link
        self.seeking_talent = seeking_talent
        self.seeking_description = seeking_description

    pass


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)), nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_venue = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='artist_show')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate # hossam do it =3

    def __init__(self, name, city, state, phone, genres,
                 image_link, facebook_link, seeking_venue, seeking_description):
        self.name = name
        self.city = city
        self.state = state
        self.phone = phone
        self.genres = genres
        self.image_link = image_link
        self.facebook_link = facebook_link
        self.seeking_venue = seeking_venue
        self.seeking_description = seeking_description

    pass


# TODO Implement Show and Artist models, and complete all model relationships and properties,
#  as a database migration.
# here i make new table Show with two Foreign Keys
# to connect with Artist, Venue table
class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, artist_id, venue_id, start_time):
        self.artist_id = artist_id
        self.venue_id = venue_id
        self.start_time = start_time

    def __repr__(self):
        return '<Show {} {}>'.format(self.artist_id, self.venue_id)

    pass
