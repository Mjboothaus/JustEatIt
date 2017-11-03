import yummly

# default option values
TIMEOUT = 15.0
RETRIES = 2

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017
API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'


# TODO: Look at saving down / caching queries for re-use to avoid using up too many queries
# TODO: Can I use the Beaker library for this? http://beaker.readthedocs.io/en/latest/index.html

# TODO: Caching: The API supports caching through the use of the ETag and Last-Modified
# response headers and the corresponding If-None-Match and If-Modified-Since request headers.
# Clients are encouraged to use these to improve performance. The API will return status code 304
# if the cached data is still valid.

def get_top_cuisines(profile):
    search_terms = profile
    top_cuisines = get_recipes(search_terms)
    return top_cuisines


def get_recipes(search_terms):

    #restricted_ingredients = request.form.get('search_terms')
    #dietary_choice = request.form.get('dietary_choice')\
    try:

        # Yummly API info - see https://github.com/dgilland/yummly.py

        client = yummly.Client(api_id = API_ID, api_key = API_KEY, timeout = TIMEOUT, retries = RETRIES)
        search = client.search(search_terms)

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
        #
        # search = client.search(**params)

        match = search.matches[0]
        recipe = client.recipe(match.id)

    except:
        pass

