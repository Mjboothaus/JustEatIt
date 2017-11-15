
# coding: utf-8

# ### Imports

# In[1]:


import pandas as pd


# ### Yummly set-up

# In[2]:


import yummly
from yummly.models import MetaCuisine

# default option values
TIMEOUT = 45.0
RETRIES = 3

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'


# ### Create Yummly Client (if necessary)

# In[4]:

client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)

try:
    print "Client API ID = " + client.api_id
    print "Yummly Client already created"
except:
    print "Created Yummly API Client"
    client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)


# ### Extract recognised cuisine-types into dataframe

# In[5]:


cuisine_list = client.metadata('cuisine')

undefined_cuisine = MetaCuisine(**{'name': u'Undefined', 'searchValue': u'cuisine^cuisine-undefined', 'id': u'cuisine-undefined', 'type': u'cuisine', 'localesAvailableIn': [u'en-US'], 'description': u'Undefined'})

cuisine_df = pd.DataFrame(cuisine_list + [undefined_cuisine])

print str(len(cuisine_list)+1) + ' recognised cuisine types (including Undefined type)'


# ### Import Country / Cuisine mappings


xls_filepath = 'country_info.xlsx'

country_info_df = pd.read_excel(xls_filepath, sheetname='Export')

country_info_df = country_info_df.drop('Cuisine_v2 [allowing multiple cuisine per country]', axis=1)




# In[9]:


def country_belongs_to_cusine(cuisine_type, cuisines):
    if cuisine_type in cuisines:
        return True
    else:
        return False



for cuisine in cuisine_df.name:
    if cuisine == 'Kid-Friendly':
        cuisine = 'Undefined'
    country_info_df[cuisine] = country_info_df['Cuisines'].apply(lambda x: country_belongs_to_cusine(cuisine, x))


all_cuisines = []
for cuisine in cuisine_df.name:
    if cuisine == 'Kid-Friendly':      # Can ignore - just skipped in lookup
        cuisine = 'Undefined'
    
    #print cuisine_df['searchValue'][cuisine_df['name']==cuisine].values.tolist()
    #print [cuisine]
    
    if cuisine != 'Undefined': 
        cuisine_countries = cuisine_df['searchValue'][cuisine_df['name']==cuisine].values.tolist()
    else:
        cuisine_countries = ['Undefined']
    #cuisine_countries = [cuisine]
            
    tmp_df = country_info_df[country_info_df[cuisine] == True]
    
    cuisine_countries.append(tmp_df['Code'].values.tolist())
    #cuisine_countries.append(tmp_df['Country'].values.tolist())

    #print cuisine_countries
    all_cuisines.append(cuisine_countries)


cuisine_by_country_df = pd.DataFrame.from_records(all_cuisines)

cuisine_by_country_df.columns = ['searchValue', 'country_list']

cuisine_id = cuisine_df['searchValue'].values.tolist()


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
        n_recipes = e.message            # error value
        pass
    
    return n_recipes


# ### Define Allergy profiles

# In[16]:


allergy_profiles = [['milk'], ['egg'], ['peanut'], ['milk, egg'],
                    ['milk, peanut'], ['egg, peanut'], ['egg, milk, peanut']] 


# In[17]:


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
            #print cuisine
            n_recipes_total = get_number_of_recipes_for_cuisine(cuisine, allergens='')
            #print n_recipes_total
            # Then query number of recipes without allergens
            n_recipes_allowed = get_number_of_recipes_for_cuisine(cuisine, allergy_profile)
            #print n_recipes_allowed
            allergy_index.append((cuisine, round(100.*float(n_recipes_allowed)/float(n_recipes_total), 1)))
            
    allergy_index.append(('cuisine^cuisine-undefined', 0.0))
    
    return allergy_index



allergy_index = calculate_cuisine_allergy_indices(allergy_profiles[3][0], cuisine_id)
#allergy_index = calculate_cuisine_allergy_indices('milk, egg', ['cuisine^cuisine-chinese'])

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
        return allergy_index_df['allergy_index'][allergy_index_df['searchValue'] == searchValue].values.tolist()[0]
    except:
        return 'Error: ' + searchValue
    

country_info_df['searchValue'] = country_info_df['Cuisines'].apply(lambda cuisine: map_cuisine_name_to_searchValue(unicode(cuisine), cuisine_df))


country_data_plt_df = country_info_df[['Country', 'Code', 'Cuisines', 'searchValue']]


country_data_plt_df['allergy_index'] = country_data_plt_df['searchValue'].apply(lambda searchValue: lookup_allergy_index_from_searchValue(searchValue, allergy_index_df))


country_data_plt_df['Code'] = country_data_plt_df['Code'].apply(lambda x: x.encode('ascii'))


country_data_list = country_data_plt_df[['Code', 'allergy_index']].values.tolist()





