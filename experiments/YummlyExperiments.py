
import yummly
import pandas as pd

# default option values
TIMEOUT = 30.0
RETRIES = 2

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'


def get_number_of_recipes_for_cuisine(cuisine_type, allergens):
    n_recipes = 0
    try:
        if allergens == '':
            search_params = {
                'q': '',
                'allowedCuisine': 'cuisine^' + cuisine_type
            }
        else:
            # print allergens
            excludeStr = ''
            for allergen in allergens.split(','):
                excludeStr += '&excludedIngredient=' + allergen.lstrip().rstrip()
                # print excludeStr
            excludeStr = excludeStr[len('&excludedIngredient='):]
            search_params = {
                'q': '',
                'allowedCuisine': 'cuisine^' + cuisine_type,
                'excludedIngredient': excludeStr
            }
            print excludeStr

        client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)
        search_results = client.search(**search_params)
        n_recipes = search_results.totalMatchCount

    except:
        n_recipes = -1  # error value
        pass

    return n_recipes

tmp = get_number_of_recipes_for_cuisine('cuisine-american', 'egg, milk')

tmp = get_number_of_recipes_for_cuisine('cuisine-american', 'egg')



quit()

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



metadata = {i+1:key for i, key in enumerate(METADATA_KEYS)}


metadata_rev = dict((v, k) for k, v in metadata.items())

client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)

ingredient_list = client.metadata('ingredient')
diet_list = client.metadata('diet')
source_list = client.metadata('source')

meta = ['']
for i in range(1, 10):
    meta.append(client.metadata(metadata[i]))



#NOTE: Something weird with 'restriction' meta type -- need to check API docs

meta_dfs = ['']

for i in range(1, 10):
    print metadata[i], len(meta[i])
    meta_dfs.append(pd.DataFrame(meta[i]))



ingredients = pd.DataFrame(ingredient_list)



metadata[metadata_rev['ingredient']]



ingredients.head(5)


diets = pd.DataFrame(diet_list)