import pandas as pd
import yummly
import os

# ### Yummly set-up

# default option values

TIMEOUT = 45.0
RETRIES = 3

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'

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
        n_recipes = e.message            # error value
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



###### -- Unused code ---------------------------------------------------------

# def search_yummly(query, cuisine_list, maxResult):
#     try:
#         search_params = {
#             'q': query,
#             'allowedCuisine': 'cuisine^' + cuisine_list,  # Need to generalise to multiple cuisines
#             'maxResult': maxResult
#         }
#
#         client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)
#
#         search_results = client.search(**search_params)
#
#         matches = search_results.matches[0]
#
#         recipe_list = []
#         for match in matches:
#             recipe = client.recipe(match.id)
#             recipe_list.append(recipe)
#
#     except:
#         pass
#
#     return recipe_list
