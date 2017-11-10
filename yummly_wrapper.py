# Yummly API info - see https://github.com/dgilland/yummly.py

import yummly
import pandas as pd

# default option values

TIMEOUT = 15.0
RETRIES = 2

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'

client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)

METADATA_KEYS = [
    'ingredient',
    'holiday',
    'diet',
    'allergy',
    'technique',
    'cuisine',
    'course',
    'source',
    'brand',
    'restriction'
]




# response headers and the corresponding If-None-Match and If-Modified-Since request headers.
# Clients are encouraged to use these to improve performance. The API will return status code 304
# if the cached data is still valid.

# def get_top_cuisines(profile):
#     search_terms = profile
#     top_cuisines = get_recipes(search_terms)
#     return top_cuisines


def search_yummly(query, cuisine_list, maxResult):

    try:
        search_params = {
            'q': query,
            'cuisine': cuisine_list,
            'maxResult': maxResult
        }

        client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)

        search_results = client.search(**search_params)

        matches = search_results.matches[0]

        recipe_list = []
        for match in matches:
            recipe = client.recipe(match.id)
            recipe_list.append(recipe)

    except:
        pass



## NOTES:

    # TODO: Look at saving down / caching queries for re-use to avoid using up too many queries
    # TODO: Can I use the Beaker library for this? http://beaker.readthedocs.io/en/latest/index.html
    # TODO: Caching: The API supports caching through the use of the ETag and Last-Modified


## INFORMATION:

        # Syntax of Yummly Python wrapper dictionary for queries

        # params = dict()
        #
        # params['q'] = search_terms
        # params['start'] = 0
        # params['maxResult'] = 10
        # params['requirePicutres'] = True
        # params['allowedIngredient[]'] = ['salt']
        # params['excludedIngredient[]'] = ['']
        # params['maxTotalTimeInSeconds'] = 3600
        # params['facetField[]'] = ['ingredient', 'diet']
        # params['flavor.meaty.min'] = 0.5
        # params['flavor.meaty.max'] = 1
        # params['flavor.sweet.min'] = 0
        # params['flavor.sweet.max'] = 0.5
        # params['nutrition.FAT.min'] = 0
        # params['nutrition.FAT.max'] = 15
