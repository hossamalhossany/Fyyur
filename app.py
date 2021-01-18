# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import (Flask, render_template, request,
                   Response, flash, redirect, url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import text
from flask_migrate import Migrate
from sqlalchemy.orm import session
from datetime import datetime
from models import db, Venue, Artist, Show


import Config

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object(Config)
moment = Moment(app)
db.init_app(app)
migrate = Migrate(app, db)



# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#


def format_datetime(value, format_date='medium'):
    date = dateutil.parser.parse(str(value))
    if format_date == 'full':
        format_date = "EEEE MMMM, d, y 'at' h:mma"
    elif format_date == 'medium':
        format_date = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format_date, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data. # hossam do it=5
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # here i use SQLAlchemy ORM  statement to get all venues
    #
    venue_list = []
    all_venues = Venue.query.all()
    for venue in all_venues:
        venue_list.append(venue)
    return render_template('pages/venues.html', venues=venue_list)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. # hossam do it =6
    # search for Hop should return "The Musical Hop".

    venue_list = []
    all_venues = Venue.query.filter(Venue.name.ilike("%" + request.form.get('search_term') + "%")).all()
    for venue in all_venues:
        venue_list.append(venue)

    return render_template('pages/search_venues.html', results=venue_list,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id # hossam dpo it = 7
    #######
    # get venue data from venue table by id
    venue = Venue.query.filter_by(id=venue_id).first_or_404()

    ###################
    # get all past shows and put them on list
    past_shows = []
    past_shows_get_all = db.session.query(Show).join(Artist).filter(
        Show.venue_id == venue.id, Show.start_time < datetime.now()
    ).all()

    for show in past_shows_get_all:
        past_shows.append({
            'artist_id': show.artist_id,
            # 'artist_name': show.artist.name,
            # 'artist_image_link': Show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        })

        ############################

        # get all incoming shows and put them on list
        upcoming_shows = []
        incoming_shows_get_all = db.session.query(Show).join(Artist).filter(
            Show.venue_id == venue.id, Show.start_time > datetime.now()
        ).all()

        for show in incoming_shows_get_all:
            upcoming_shows.append({
                'artist_id': show.artist_id,
                'artist_name': show.artist.name,
                'artist_image_link': show.artist.image_link,
                'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
            })
    ############################
    # append all data to data to send to html page
    data = [{
        'id': venue.id,
        'venue_name': venue.name,
        'venue_city': venue.city,
        'venue_state': venue.state,
        'venue_address': venue.address,
        'venue_phone': venue.phone,
        'venue_genres': venue.genres,
        'venue_image_link': venue.image_link,
        'venue_facebook_link': venue.facebook_link,
        'venue_seeking_talent': venue.seeking_talent,
        'venue_seeking_description': venue.seeking_description,

        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }]

    ##############################

    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    # TODO: insert form data as a new Venue record in the db, instead # hossam do it = 8
    # TODO: modify data to be the data object returned from db insertion # hossam do it = 9
    # add new venue

    form = VenueForm(request.form)
    venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        address=form.address.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_description=form.seeking_description.data
    )
    try:
        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + venue.name + ' was successfully listed!')
        return render_template('pages/home.html')
    except ValueError as e:
        flash("some error happen")
        db.session.rollback()
    finally:
        db.session.close()


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database # hossam do it = 12
    # get all artists

    artist_list = []
    all_artists = Artist.query.all()
    for artist in all_artists:
        artist_list.append(artist)
    return render_template('pages/artists.html', artists=artist_list)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. # hossam do it =13
    # search for 'A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".

    artist_list = []
    all_artists = Artist.query.filter(Artist.name.ilike("%" + request.form.get('search_term') + "%")).all()
    for artist in all_artists:
        artist_list.append(artist)

    return render_template('pages/search_artists.html', results=artist_list,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # TODO: replace with real venue data from the venues table, using artist_id # hossam do it =14
    #######

    # get artist data from artist table by id
    artist = Artist.query.filter_by(id=artist_id).first_or_404()

    ###################
    # get all past shows and put them on list
    past_shows = []
    past_shows_get_all = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist.id, Show.start_time < datetime.now()
    ).all()

    for show in past_shows_get_all:
        past_shows.append({
            'venue_id': show.venue_id,
            # 'artist_name': show.artist.name,
            # 'artist_image_link': Show.artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        })

        ############################

    # get all incoming shows and put them on list
    upcoming_shows = []
    incoming_shows_get_all = db.session.query(Show).join(Venue).filter(
        Show.artist_id == artist.id, Show.start_time > datetime.now()
    ).all()

    for show in incoming_shows_get_all:
        upcoming_shows.append({
            'venue_id': show.venue_id,
            # 'venue_name': show.venue.name,
            # 'venue_image_link': show.venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        })
    ############################
    # append all data to data to send to html page
    data = [{
        'id': artist.id,
        'artist_name': artist.name,
        'artist_city': artist.city,
        'artist_state': artist.state,
        'artist_phone': artist.phone,
        'artist_genres': artist.genres,
        'artist_image_link': artist.image_link,
        'artist_facebook_link': artist.facebook_link,
        'artist_seeking_talent': artist.seeking_venue,
        'artist_seeking_description': artist.seeking_description,

        'past_shows': past_shows,
        'upcoming_shows': upcoming_shows,
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }]

    ##############################

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = '238'
    # TODO: populate form with fields from artist with ID <artist_id> # 15
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing # 16
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = '254'
    # TODO: populate form with values from venue with ID <venue_id> # 17
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing # 18
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # TODO: insert form data as a new artist record in the db, instead # hossam do it = 19
    # TODO: modify data to be the data object returned from db insertion # hossam do it = 20
    # add new artist

    form = ArtistForm(request.form)
    artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data
    )
    try:
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + artist.name + ' was successfully listed!')
        return render_template('pages/home.html')
    except ValueError as e:
        flash("some error happen")
        db.session.rollback()
    finally:
        db.session.close()


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data. # hossam do it = 22
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    # get all shows

    show_list = []
    all_shows = Show.query.all()
    for show in all_shows:
        show_list.append(show)
    return render_template('pages/shows.html', shows=show_list)


@app.route('/shows/create', methods=['GET'])
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # TODO: insert form data as a new Show record in the db, instead # hossam do it = 23

    form = ShowForm(request.form)
    show = Show(
        artist_id=form.artist_id.data,
        venue_id=form.venue_id.data,
        start_time=form.start_time.data
    )
    try:
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
        return render_template('pages/home.html')
    except ValueError as e:
        flash("some error happen")
        db.session.rollback()
    finally:
        db.session.close()


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()
# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
