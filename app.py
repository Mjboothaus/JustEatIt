# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, render_template, request, url_for
# from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from forms import *

import yummly_wrapper

import pandas as pd
import numpy as np

## import holoviews as hv      ## NOTE: For the future -- HoloViews is a nice wrapper for Bokeh
## hv.extension('bokeh')

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure


# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')
# db = SQLAlchemy(app)

# Automatically tear down SQLAlchemy.
'''
@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()
'''

# Login required decorator.
'''
def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
'''


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/allergy_profile')
def allergy_profile():
    form = SpecifyProfileForm(request.form)
    return render_template('forms/allergy_profile.html', form=form)


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/allergy_info')
def allergy_info():
    return render_template('pages/allergy_info.html')


@app.route('/bokeh')
def bokeh():

    ## Get any control input from page

    # stock_ticker = request.form.get('stock_ticker')

    ## Load any reference data e.g. list of cuisine / country

    ## Validation

    ## Load Yummly data

    data = None
    try:
        ## Get Yummly data - API call
        # output to static HTML file

        # PLACEHOLDER: circle renderer with a size, color, and alpha

        plot = figure(plot_width=400, plot_height=400)
        plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)
        script, div = components(plot)

    except Exception as e:
        return render_template('errors/bokeh_error.html', error=e.message)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return render_template('pages/bokeh.html',
                           plot_script=script,
                           plot_div=div,
                           js_resources=js_resources,
                           css_resources=css_resources)



@app.route('/top10')
def top10():
    allergy_profile = []
    allergy_profile.append(['peanut'])
    allergy_profile.append(['peanut, egg'])
    allergy_profile.append(['peanut, egg, milk'])

    for profile in allergy_profile:
        cuisines = get_top_cuisines(profile)

    return render_template('pages/top10.html')


@app.route('/eat_map')
def eat_map():
    APP_STATIC = os.path.join(basedir, 'static')

    path = APP_STATIC + 'data/country_info.csv'
    print path

    country_codes = pd.read_csv(path[1:len(path)])

    country_dict = country_codes.to_dict()

    country_data = [
        ["BLR", 75], ["BLZ", 43], ["RUS", 50], ["RWA", 88], ["SRB", 21], ["TLS", 43],
        ["REU", 21], ["TKM", 19], ["TJK", 60], ["ROU", 4], ["TKL", 44], ["GNB", 38],
        ["GUM", 67], ["GTM", 2], ["SGS", 95], ["GRC", 60], ["GNQ", 57], ["GLP", 53],
        ["JPN", 59], ["GUY", 24], ["GGY", 4], ["GUF", 21], ["GEO", 42], ["GRD", 65],
        ["GBR", 14], ["GAB", 47], ["SLV", 15], ["GIN", 19], ["GMB", 63], ["GRL", 56],
        ["ERI", 57], ["MNE", 93], ["MDA", 39], ["MDG", 71], ["MAF", 16], ["MAR", 8],
        ["MCO", 25], ["UZB", 81], ["MMR", 21], ["MLI", 95], ["MAC", 33], ["MNG", 93],
        ["MHL", 15], ["MKD", 52], ["MUS", 19], ["MLT", 69], ["MWI", 37], ["MDV", 44],
        ["MTQ", 13], ["MNP", 21], ["MSR", 89], ["MRT", 20], ["IMN", 72], ["UGA", 59],
        ["TZA", 62], ["MYS", 75], ["MEX", 80], ["ISR", 77], ["FRA", 54], ["IOT", 56],
        ["SHN", 91], ["FIN", 51], ["FJI", 22], ["FLK", 4], ["FSM", 69], ["FRO", 70],
        ["NIC", 66], ["NLD", 53], ["NOR", 7], ["NAM", 63], ["VUT", 15], ["NCL", 66],
        ["NER", 34], ["NFK", 33], ["NGA", 45], ["AUS", 96], ["NPL", 21], ["NRU", 13],
        ["NIU", 6], ["COK", 19], ["XKX", 32], ["CIV", 27], ["CHE", 65], ["COL", 64],
        ["CHN", 16], ["CMR", 70], ["CHL", 15], ["CCK", 85], ["CAN", 76], ["COG", 20],
        ["CAF", 93], ["COD", 36], ["CZE", 77], ["CYP", 65], ["CXR", 14], ["CRI", 31],
        ["CUW", 67], ["CPV", 63], ["CUB", 40], ["SWZ", 58], ["SYR", 96], ["SXM", 31]]

    return render_template('pages/eat_map.html', country_data=country_data)


@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@app.route('/register')
def register():
    form = RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@app.route('/forgot')
def forgot():
    form = ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)


# Error handlers.


@app.errorhandler(500)
def internal_error(error):
    # db_session.rollback()
    return render_template('errors/500.html'), 500


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

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
