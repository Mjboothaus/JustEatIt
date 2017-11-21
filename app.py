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
from math import pi

### Yummly

import yummly
from yummly_settings import TIMEOUT, RETRIES, API_ID, API_KEY
from yummly.models import MetaCuisine

### Bokeh imports

from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.plotting import figure

# from bokeh import embed, resources, plotting

# bokeh.resources import INLINE

# from bokeh.charts import Bar    # -- NOTE: bkcharts is no longer maintained - do not use!

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


#------------------------------------------------------------------------------
#     Load/define default data if running in offline mode
#------------------------------------------------------------------------------

country_data_list = [['AFG', 83.5],
                     ['ALA', 26.3],
                     ['DZA', 91.8],
                     ['ASM', 55.8],
                     ['AIA', 87.5],
                     ['ATG', 87.5],
                     ['ARG', 87.5],
                     ['ABW', 87.5],
                     ['AUS', 30.1],
                     ['AUT', 45.6],
                     ['BHS', 87.5],
                     ['BGD', 90.3],
                     ['BRB', 87.5],
                     ['BEL', 39.2],
                     ['BLZ', 86.9],
                     ['BMU', 55.8],
                     ['BOL', 87.5],
                     ['BRA', 87.5],
                     ['VGB', 87.5],
                     ['BRN', 83.5],
                     ['BGR', 71.8],
                     ['KHM', 87.6],
                     ['CAN', 55.8],
                     ['CYM', 87.5],
                     ['CHL', 87.5],
                     ['CHN', 75.4],
                     ['HKG', 75.4],
                     ['MAC', 75.4],
                     ['CXR', 30.1],
                     ['CCK', 30.1],
                     ['COL', 87.5],
                     ['COK', 72.5],
                     ['CRI', 86.9],
                     ['CUB', 87.5],
                     ['CYP', 79.5],
                     ['CZE', 71.8],
                     ['DNK', 26.3],
                     ['DMA', 87.5],
                     ['DOM', 87.5],
                     ['ECU', 87.5],
                     ['EGY', 91.8],
                     ['SLV', 86.9],
                     ['EST', 26.3],
                     ['FLK', 30.1],
                     ['FJI', 72.5],
                     ['FIN', 26.3],
                     ['FRA', 39.2],
                     ['GUF', 87.5],
                     ['PYF', 72.5],
                     ['DEU', 45.6],
                     ['GIB', 64.8],
                     ['GRC', 79.5],
                     ['GRL', 26.3],
                     ['GRD', 87.5],
                     ['GLP', 87.5],
                     ['GUM', 55.8],
                     ['GTM', 86.9],
                     ['GGY', 30.1],
                     ['GUY', 87.5],
                     ['HTI', 87.5],
                     ['VAT', 71.0],
                     ['HND', 86.9],
                     ['HUN', 71.8],
                     ['ISL', 26.3],
                     ['IND', 90.3],
                     ['IDN', 87.6],
                     ['IRL', 50.8],
                     ['IMN', 30.1],
                     ['ITA', 71.0],
                     ['JAM', 87.5],
                     ['JPN', 76.6],
                     ['JEY', 30.1],
                     ['KIR', 72.5],
                     ['PRK', 75.4],
                     ['KOR', 75.4],
                     ['LAO', 87.6],
                     ['LVA', 71.8],
                     ['LBY', 91.8],
                     ['LIE', 45.6],
                     ['LTU', 71.8],
                     ['LUX', 45.6],
                     ['MKD', 79.5],
                     ['MYS', 83.5],
                     ['MDV', 90.3],
                     ['MLT', 91.8],
                     ['MHL', 72.5],
                     ['MTQ', 87.5],
                     ['MUS', 90.3],
                     ['MEX', 86.9],
                     ['FSM', 72.5],
                     ['MCO', 39.2],
                     ['MNG', 83.5],
                     ['MSR', 87.5],
                     ['MAR', 91.8],
                     ['MMR', 87.6],
                     ['NRU', 72.5],
                     ['NPL', 90.3],
                     ['NLD', 45.6],
                     ['ANT', 87.5],
                     ['NCL', 72.5],
                     ['NZL', 30.1],
                     ['NIC', 86.9],
                     ['NIU', 72.5],
                     ['NFK', 30.1],
                     ['NOR', 26.3],
                     ['PAK', 90.3],
                     ['PLW', 72.5],
                     ['PAN', 86.9],
                     ['PNG', 72.5],
                     ['PRY', 87.5],
                     ['PER', 87.5],
                     ['PHL', 83.5],
                     ['PCN', 30.1],
                     ['POL', 71.8],
                     ['PRT', 64.8],
                     ['PRI', 87.5],
                     ['REU', 39.2],
                     ['ROU', 71.8],
                     ['BLM', 87.5],
                     ['KNA', 87.5],
                     ['LCA', 87.5],
                     ['MAF', 87.5],
                     ['VCT', 87.5],
                     ['WSM', 72.5],
                     ['SYC', 39.2],
                     ['SGP', 75.4],
                     ['SVK', 71.8],
                     ['SVN', 71.8],
                     ['SLB', 72.5],
                     ['ZAF', 30.1],
                     ['SSD', 91.8],
                     ['ESP', 78.5],
                     ['LKA', 90.3],
                     ['SDN', 91.8],
                     ['SUR', 87.5],
                     ['SWE', 26.3],
                     ['CHE', 39.2],
                     ['TWN', 75.4],
                     ['THA', 87.6],
                     ['TLS', 72.5],
                     ['TKL', 72.5],
                     ['TON', 72.5],
                     ['TTO', 87.5],
                     ['TUN', 91.8],
                     ['TUR', 87.6],
                     ['TCA', 87.5],
                     ['TUV', 72.5],
                     ['GBR', 30.1],
                     ['USA', 55.8],
                     ['UMI', 55.8],
                     ['URY', 87.5],
                     ['VUT', 72.5],
                     ['VEN', 87.5],
                     ['VNM', 75.4],
                     ['VIR', 55.8],
                     ['WLF', 72.5],
                     ['ESH', 91.8]]



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
        return render_template('pages/eat_map.html', allergy_profile_choice=choice,
                               country_data=country_data_list)
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


@app.route('/top10')
def top10():
    # TODO: Can you pass the data through the function argument?

    ## Load any reference data e.g. list of cuisine / country

    ## Validation

    ## Load Yummly data

    data = None
    try:
        ## Get Yummly data - API call
        # output to static HTML file

        # top15_destinations = country_data_plt_df.sort_values('allergy_index', ascending=False).iloc[0:15]

        top15_list = [[u'Egypt', 'EGY', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Algeria', 'DZA', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Morocco', 'MAR', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'South Sudan', 'SSD', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Western Sahara', 'ESH', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Malta', 'MLT', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Sudan', 'SDN', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Tunisia', 'TUN', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'Libya', 'LBY', u'Moroccan', u'cuisine^cuisine-moroccan', 91.8],
                      [u'India', 'IND', u'Indian', u'cuisine^cuisine-indian', 90.3],
                      [u'Maldives', 'MDV', u'Indian', u'cuisine^cuisine-indian', 90.3],
                      [u'Pakistan', 'PAK', u'Indian', u'cuisine^cuisine-indian', 90.3],
                      [u'Mauritius', 'MUS', u'Indian', u'cuisine^cuisine-indian', 90.3],
                      [u'Nepal', 'NPL', u'Indian', u'cuisine^cuisine-indian', 90.3],
                      [u'Bangladesh', 'BGD', u'Indian', u'cuisine^cuisine-indian', 90.3]]

        top15_list_df = pd.DataFrame(top15_list)
        top15_list_df.columns = ['Country', 'Code', 'Cuisines', 'searchValue', 'allergy_index']

        #plot_top15 = Bar(top15_list_df, label='Country', values='allergy_index', legend=False)
        #plot_top15.add_labels('y', 'Allergy Index')

        p = figure(x_range=top15_list_df.Country.values.tolist(), plot_height=450, title="")

        p.vbar(x=top15_list_df.Country.values.tolist(), top=top15_list_df.allergy_index.values, width=0.9)

        p.xaxis.major_label_orientation = pi / 2
        p.xgrid.grid_line_color = None
        p.y_range.start = 0
        p.y_range.end = 100

        script, div = components(p)

    except Exception as e:
        return render_template('errors/bokeh_error.html', error=e.message)

    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    return render_template('pages/top10.html',
                           plot_script=script,
                           plot_div=div,
                           js_resources=js_resources,
                           css_resources=css_resources)


@app.route('/eat_map')
def eat_map():
    # ### Import Country / Cuisine mappings

    """
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

        undefined_cuisine = MetaCuisine(
            **{'name': u'Undefined', 'searchValue': u'cuisine^cuisine-undefined', 'id': u'cuisine-undefined',
               'type': u'cuisine', 'localesAvailableIn': [u'en-US'], 'description': u'Undefined'})

        cuisine_df = pd.DataFrame(cuisine_list + [undefined_cuisine])

        print str(len(cuisine_list) + 1) + ' recognised cuisine types (including Undefined type)'

        country_info_df = pd.read_excel(xls_filepath, sheetname='Export')

        country_info_df = country_info_df.drop('Cuisine_v2 [allowing multiple cuisine per country]', axis=1)

        for cuisine in cuisine_df.name:
            if cuisine == 'Kid-Friendly':
                cuisine = 'Undefined'
            country_info_df[cuisine] = country_info_df['Cuisines'].apply(
                lambda x: country_belongs_to_cusine(cuisine, x))

        all_cuisines = []
        for cuisine in cuisine_df.name:
            if cuisine == 'Kid-Friendly':  # Can ignore - just skipped in lookup
                cuisine = 'Undefined'

            # print cuisine_df['searchValue'][cuisine_df['name']==cuisine].values.tolist()
            # print [cuisine]

            if cuisine != 'Undefined':
                cuisine_countries = cuisine_df['searchValue'][cuisine_df['name'] == cuisine].values.tolist()
            else:
                cuisine_countries = ['Undefined']
            # cuisine_countries = [cuisine]

            tmp_df = country_info_df[country_info_df[cuisine] == True]

            cuisine_countries.append(tmp_df['Code'].values.tolist())
            # cuisine_countries.append(tmp_df['Country'].values.tolist())

            # print cuisine_countries
            all_cuisines.append(cuisine_countries)

        cuisine_by_country_df = pd.DataFrame.from_records(all_cuisines)

        cuisine_by_country_df.columns = ['searchValue', 'country_list']

        cuisine_id = cuisine_df['searchValue'].values.tolist()

        return cuisine_df, cuisine_by_country_df

        # Note: Working with cuisine ID column as this maps directly to the searchValue column by adding the suffix
        #       'cuisine^'

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
                              'cuisine^cuisine-cajun',
                              'cuisine^cuisine-undefined']
            for cuisine in cuisine_list:
                if cuisine not in ignore_cuisine:
                    # First query total number of recipes for the cuisine
                    # print cuisine
                    n_recipes_total = get_number_of_recipes_for_cuisine(cuisine, allergens='')
                    # print n_recipes_total
                    # Then query number of recipes without allergens
                    n_recipes_allowed = get_number_of_recipes_for_cuisine(cuisine, allergy_profile)
                    # print n_recipes_allowed
                    allergy_index.append((cuisine, round(100. * float(n_recipes_allowed) / float(n_recipes_total), 1)))

            allergy_index.append(('cuisine^cuisine-undefined', 0.0))

            return allergy_index

        allergy_index = calculate_cuisine_allergy_indices(allergy_profiles[3][0], cuisine_id)
        # allergy_index = calculate_cuisine_allergy_indices('milk, egg', ['cuisine^cuisine-chinese'])

        # TODO: Need to pass in the chosen allergy profile


        allergy_index_df = pd.DataFrame(allergy_index)
        allergy_index_df.columns = ['searchValue', 'allergy_index']

        def map_cuisine_name_to_searchValue(cuisine_name, cuisine_df):
            try:
                return cuisine_df['searchValue'][cuisine_df['name'] == cuisine_name].values.tolist()[0]
            except:
                return 'Error: ' + cuisine_name

        def lookup_allergy_index_from_searchValue(searchValue, allergy_index_df):
            try:
                return \
                    allergy_index_df['allergy_index'][allergy_index_df['searchValue'] == searchValue].values.tolist()[0]
            except:
                return 'Error: ' + searchValue

    country_info_df['searchValue'] = country_info_df['Cuisines'].apply(
        lambda cuisine: map_cuisine_name_to_searchValue(unicode(cuisine), cuisine_df))

    country_data_plt_df = country_info_df[['Country', 'Code', 'Cuisines', 'searchValue']]

    country_data_plt_df['allergy_index'] = country_data_plt_df['searchValue'].apply(
        lambda searchValue: lookup_allergy_index_from_searchValue(searchValue, allergy_index_df))

    country_data_plt_df['Code'] = country_data_plt_df['Code'].apply(lambda x: x.encode('ascii'))

    country_data_list = country_data_plt_df[['Code', 'allergy_index']].values.tolist()

    # ### Define static info

    basedir = os.path.abspath(os.path.dirname(__file__))
    APP_STATIC = os.path.join(basedir, 'static')
    xls_filepath = APP_STATIC + '/data/country_info.xlsx'

    allergy_profiles = [['milk'], ['egg'], ['peanut'], ['milk, egg'],
                        ['milk, peanut'], ['egg, peanut'], ['egg, milk, peanut']]

    selected_profile = allergy_profiles[3][0]

    # TODO: Remove above once passed through (need to convert index# to allergy list of ingredients)

    cuisine_df, cuisine_by_country_df = import_country_and_cuisine_info(xls_filepath, API_ID)

    cuisine_id = cuisine_df['searchValue'].values.tolist()

    allergy_indices = calculate_cuisine_allergy_indices(selected_profile, cuisine_id)

    """

    return render_template('pages/eat_map.html', country_data=country_data_list)


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
