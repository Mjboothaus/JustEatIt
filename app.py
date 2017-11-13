# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

### Flask

from flask import Flask, render_template, request, url_for
from forms import *
# from flask.ext.sqlalchemy import SQLAlchemy

### General

import os
import pandas as pd
from logging import Formatter, FileHandler
import logging

### Yummly

import yummly
from yummly_settings import TIMEOUT, RETRIES, API_ID, API_KEY

### Bokeh imports

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure

### Unused

# import numpy as np
# from random import random, randint, seed


# ----------------------------------------------------------------------------#
# App Configuaration
# ----------------------------------------------------------------------------#

app = Flask(__name__)
app.config.from_object('config')

### Database backend -- currently disabled

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
# App routes
# ----------------------------------------------------------------------------#


@app.route('/')
def home():
    return render_template('pages/home.html')


@app.route('/allergy_profile', methods=['GET', 'POST'])
def allergy_profile():
    form = SpecifyProfileForm(request.form)
    if request.method == 'POST':
        choice = form.profile.data
        return render_template('pages/eat_map.html', allergy_profile_choice=choice)
    else:
        return render_template('forms/allergy_profile.html', form=form)


@app.route('/about')
def about():
    return render_template('pages/about.html')


@app.route('/version')
def version():
    return render_template('pages/version.html')

@app.route('/allergy_info')
def allergy_info():
    return render_template('pages/allergy_info.html')


@app.route('/bokeh')
def bokeh():

    # TODO: Implement another viz -- for now maybe Top 10 countries & allergy index

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



# @app.route('/top10')
# def top10():
#     allergy_profile = []
#     allergy_profile.append(['peanut'])
#     allergy_profile.append(['peanut, egg'])
#     allergy_profile.append(['peanut, egg, milk'])
#
#     for profile in allergy_profile:
#         cuisines = get_top_cuisines(profile)
#
#     return render_template('pages/top10.html')


@app.route('/eat_map')
def eat_map():

    # ### Import Country / Cuisine mappings

    def country_belongs_to_cusine(cuisine_type, cuisines):
        if cuisine_type in cuisines:
            return True
        else:
            return False

    def connect_to_yummly():
        try:
            client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)
            return client
        except Exception as e:
            return e.message

    def import_country_and_cuisine_info(xls_filepath, API_ID):

        # ### Extract recognised cuisine-types into dataframe

        client = connect_to_yummly()

        if client.api_id == API_ID:
            cuisine_list = client.metadata('cuisine')
        else:
            pass
            # TODO: Should pass an error back to webpage if unable to connect to Yummly.

        cuisine_df = pd.DataFrame(cuisine_list)

        print str(len(cuisine_list)) + ' recognised cuisine types'

        country_info = pd.read_excel(xls_filepath, sheetname='Export',
                                     names={'Country', 'Code', 'Region', 'Cuisines'})

        for cuisine in cuisine_df.name:
            if cuisine == 'Kid-Friendly':
                cuisine = 'Undefined'
            country_info[cuisine] = country_info['Cuisines'].apply(lambda x: country_belongs_to_cusine(cuisine, x))

        all_cuisines = []
        for cuisine in cuisine_df.name:
            if cuisine == 'Kid-Friendly':
                cuisine = 'Undefined'
            cuisine_countries = [cuisine]
            tmp_df = country_info[country_info[cuisine] == True]
            cuisine_countries.append(tmp_df['Country'].values.tolist())
            all_cuisines.append(cuisine_countries)

        cuisine_by_country_df = pd.DataFrame(all_cuisines)

        # e.g. cuisine_df['searchValue'][cuisine_df['description'] == 'American'][0]

        return cuisine_df, cuisine_by_country_df

    # Note: Working with cuisine ID column as this maps directly to the searchValue column


    def get_number_of_recipes_for_cuisine(cuisine_id, allergens):
        n_recipes = 0
        try:
            if allergens == '':
                search_params = {
                    'q': '',
                    'allowedCuisine': cuisine_id
                }
            else:
                search_params = {
                    'q': '',
                    'allowedCuisine': cuisine_id
                }

                allergen_list = []
                for allergen in allergens.split(','):
                    allergen_list.append(allergen.lstrip().rstrip())
                search_params['excludedIngredient'] = allergen_list

            client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)
            search_results = client.search(**search_params)
            n_recipes = search_results.totalMatchCount

        except Exception as e:
            n_recipes = e.message  # error value
            pass

        return n_recipes

    # Example URL query

    # https://www.yummly.com/recipes?allowedCuisine=cuisine%5Ecuisine-american&excludedIngredient=egg&excludedIngredient=milk

    ### Allergy index calculation notes

    # For each cuisine-type - A = query total #recipes and B = total #recipes without all allergen ingredients (in allergy profile)

    # Calculate allergy (quotient) index as B/A. If there are a lot of recipes in that cuisine type without allergens
    # then B is approximately equal to A and the quotient is close to 100% ( => allergy-friendly cuisine).

    # Similarly could calculate a 2nd metric where (for more than one allergen in profile) you drop one of the allergens
    # at a time from the allergy profile to see the change/impact. The Eat Map could toggle between STRICT and RELAXED mode.

    def calculate_cuisine_allergy_indices(allergy_profile, cuisine_list):
        allergy_index = []
        ignore_cuisine = ['cuisine^cuisine-kid-friendly',
                          'cuisine^cuisine-southern',
                          'cuisine^cuisine-southwestern',
                          'cuisine^cuisine-barbecue-bbq',
                          'cuisine^cuisine-cajun']
        for cuisine in cuisine_list:
            if cuisine not in ignore_cuisine:
                # First query total number of recipes for the cuisine
                n_recipes_total = get_number_of_recipes_for_cuisine(cuisine, allergens='')

                # Then query number of recipes without allergens
                n_recipes_allowed = get_number_of_recipes_for_cuisine(cuisine, allergy_profile)
                allergy_index.append((cuisine, round(100. * float(n_recipes_allowed) / float(n_recipes_total), 1)))

        return allergy_index

    # ### Define static info

    basedir = os.path.abspath(os.path.dirname(__file__))
    APP_STATIC = os.path.join(basedir, 'static')
    xls_filepath = APP_STATIC + '/data/country_info.xlsx'

    allergy_profiles = [['milk'], ['egg'], ['peanut'], ['milk, egg'],
                        ['milk, peanut'], ['egg, peanut'], ['egg, milk, peanut']]

    selected_profile = allergy_profiles[3][0]

    # TODO: Remove above once passed through


    cuisine_df, cuisine_by_country_df = import_country_and_cuisine_info(xls_filepath, API_ID)

    cuisine_id = cuisine_df['searchValue'].values.tolist()

    allergy_indices = calculate_cuisine_allergy_indices(selected_profile, cuisine_id)

    # e.g. allergy_index = calculate_cuisine_allergy_indices('milk, egg', ['cuisine^cuisine-chinese'])

    # TODO: Populate the country_data_for_map array with lookup from tables

    # country_data_for_map = country_codes[['Code', 'AllergyIndex']].values.tolist()

    country_data_for_map = None

    return render_template('pages/eat_map.html', country_data=country_data_for_map)


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


# ----------------------------------------------------------------------------#
# Error Handling pages
# ----------------------------------------------------------------------------#

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
# Launch App
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''

# ----------------------------------------------------------------------------#
# Left over prototyping code
# ----------------------------------------------------------------------------#


## This was code to put random values into the country data array for the country map

# csv_filepath = APP_STATIC + '/data/country_info.csv'

# seed(42)      # Set a constant starting seed

# country_codes = pd.read_csv(csv_filepath, header=0, names={'Country', 'Code'})

# country_codes['AllergyIndex'] = country_codes['Code'].apply(lambda x: randint(0, len(country_codes)))

# country_data_for_map = country_codes[['Code', 'AllergyIndex']].values.tolist()
# country_data = [
#     ["BLR", 75], ["BLZ", 43], ["RUS", 50], ["RWA", 88], ["SRB", 21], ["TLS", 43],
#     ["REU", 21], ["TKM", 19], ["TJK", 60], ["ROU", 4], ["TKL", 44], ["GNB", 38],
#     ["GUM", 67], ["GTM", 2], ["SGS", 95], ["GRC", 60], ["GNQ", 57], ["GLP", 53],
#     ["JPN", 59], ["GUY", 24], ["GGY", 4], ["GUF", 21], ["GEO", 42], ["GRD", 65],
#     ["GBR", 14], ["GAB", 47], ["SLV", 15], ["GIN", 19], ["GMB", 63], ["GRL", 56],
#     ["ERI", 57], ["MNE", 93], ["MDA", 39], ["MDG", 71], ["MAF", 16], ["MAR", 8],
#     ["MCO", 25], ["UZB", 81], ["MMR", 21], ["MLI", 95], ["MAC", 33], ["MNG", 93],
#     ["MHL", 15], ["MKD", 52], ["MUS", 19], ["MLT", 69], ["MWI", 37], ["MDV", 44],
#     ["MTQ", 13], ["MNP", 21], ["MSR", 89], ["MRT", 20], ["IMN", 72], ["UGA", 59],
#     ["TZA", 62], ["MYS", 75], ["MEX", 80], ["ISR", 77], ["FRA", 54], ["IOT", 56],
#     ["SHN", 91], ["FIN", 51], ["FJI", 22], ["FLK", 4], ["FSM", 69], ["FRO", 70],
#     ["NIC", 66], ["NLD", 53], ["NOR", 7], ["NAM", 63], ["VUT", 15], ["NCL", 66],
#     ["NER", 34], ["NFK", 33], ["NGA", 45], ["AUS", 96], ["NPL", 21], ["NRU", 13],
#     ["NIU", 6], ["COK", 19], ["XKX", 32], ["CIV", 27], ["CHE", 65], ["COL", 64],
#     ["CHN", 16], ["CMR", 70], ["CHL", 15], ["CCK", 85], ["CAN", 76], ["COG", 20],
#     ["CAF", 93], ["COD", 36], ["CZE", 77], ["CYP", 65], ["CXR", 14], ["CRI", 31],
#     ["CUW", 67], ["CPV", 63], ["CUB", 40], ["SWZ", 58], ["SYR", 96], ["SXM", 31]]