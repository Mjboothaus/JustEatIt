
# coding: utf-8

# In[ ]:


import yummly
import pandas as pd

# default option values
TIMEOUT = 30.0
RETRIES = 2

# Yummly mjboothaus Account: Hackathon Plan - Access granted 24 July 2017

API_ID = 'b4f167ed'
API_KEY = 'f69184af19beb4b76e7b7b1984046581'


# In[77]:


client = yummly.Client(api_id=API_ID, api_key=API_KEY, timeout=TIMEOUT, retries=RETRIES)


# In[84]:


client.URL_GET


# In[ ]:





# In[ ]:





# In[76]:


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


# In[ ]:





# In[ ]:





# In[3]:


metadata = {i+1:key for i, key in enumerate(METADATA_KEYS)}


# In[4]:


metadata_rev = dict((v, k) for k, v in metadata.items())


# In[5]:


metadata_rev


# In[6]:


metadata


# In[7]:


metadata[3]


# In[8]:


ingredient_list = client.metadata('ingredient')
diet_list = client.metadata('diet')
source_list = client.metadata('source')

meta = ['']
for i in range(1, 10):
    meta.append(client.metadata(metadata[i]))


# In[9]:


#NOTE: Something weird with 'restriction' meta type -- need to check API docs

meta_dfs = ['']

for i in range(1, 10):
    print metadata[i], len(meta[i])
    meta_dfs.append(pd.DataFrame(meta[i]))


# In[10]:


print meta[2][0:2]


# In[11]:


#for i in range(1, 10):
#    print str(i) + ': ' + metadata[i] + ' (' + str(len(meta[i])) + ') -----------------------------------------------'
#    print meta_dfs[i].head(min(4, len(meta[i])))
#    # print '--------------------------------------------------------------------'


# In[12]:


#type(ingredient_list)


# In[13]:


ingredients = pd.DataFrame(ingredient_list)


# In[14]:


metadata[metadata_rev['ingredient']]


# In[15]:


ingredients.head(5)


# In[16]:


diets = pd.DataFrame(diet_list)


# In[17]:


diets


# In[18]:


search_params = {
    'q': '',
    'cuisine': 'American',
    'maxResult': 10000     # 100000
}


# In[19]:


search_params


# In[20]:


# Start to look at recipes

#results = client.search(query_str, maxResults=100000)

results = client.search(**search_params)

print 'Total Matches:', results.totalMatchCount

#for match in results.matches:
#        print 'Recipe ID:', match.id
#        print 'Recipe:', match.recipeName
#        print 'Rating:', match.rating
#        # print 'Total Time (mins):' + match.TOTAL_TIME_MISSING / 60.0)
#        print '----------------------------------------------------'


# In[21]:


type(results.matches)


# In[22]:


len(results.matches)


# In[23]:


results.matches[0].id


# In[ ]:





# In[24]:


from time import sleep


# In[25]:


recipes = []
for match in results.matches:    
    this_recipe = []
    recipe = client.recipe(match.id)
    sleep(1.0)
    for ingred in recipe.ingredientLines:
        this_recipe.append(ingred)
    recipes.append(this_recipe)


# In[26]:


recipes_df = pd.DataFrame(recipes)


# In[27]:


recipes_df.head(10)


# In[28]:


recipes_df.info()


# In[29]:


recipes_df.describe()


# In[30]:


## Comment: need to standardise ingredients - see NYTimes approach
# Probably can use spaCy
# Will need to clean the text as part of this and have some sort of similarity measure for ingredients


# In[31]:


type(recipes_df.iloc[0])


# In[32]:


import spacy
nlp = spacy.load('en')


# In[34]:


def get_entity_and_type(textstr):
    textstr = unicode(textstr)
    doc = nlp(textstr)
    out_list = []
    for ent in doc.ents:
        out_list.append((ent, ent.label_, ent.label, ent.orth_)) 
    return out_list


# token.orth_, token.ent_type_ if token.ent_type_


# In[72]:


# doc = nlp(u'London is a big city in the United Kingdom.')

def standardise_recipe_ingredients(ingredient):
    print ingredient
    ingred_doc = nlp(ingredient)
    for i, word in enumerate(ingredient.split(' ')):
        print word, (ingred_doc[i].text, ingred_doc[i].ent_type_)
        
        #print ingred    #.text     #, ingred[0].ent_iob, ingred[0].ent_type_


# In[73]:


example_ingred = recipes_df[0][2]


# In[74]:


standardise_recipe_ingredients(example_ingred)


# In[35]:


doc1 = nlp(recipes_df[0][2])


# In[ ]:


recipes_df[0][2]


# In[50]:


doc = nlp(u'London is a big city in the United Kingdom.')
len(doc)
print(doc[0].text, doc[0].ent_iob, doc[0].ent_type_)
# (u'London', 2, u'GPE')
print(doc[1].text, doc[1].ent_iob, doc[1].ent_type_)
# (u'is', 3, u'')


# In[46]:


# In[40]:


type(doc1)


# In[ ]:





# In[ ]:





# In[94]:


for ent in doc1.ents:
       for word in ent.sent:
           print word


# In[90]:


for chunk in doc1.noun_chunks:
    print chunk


# In[49]:


for i in range(0, 10):
    print recipes_df[0][i]


# In[61]:


recipes_df['spacy-ingreds'] = recipes_df[0].apply(lambda ingred : get_entity_and_type(ingred))


# In[62]:


print recipes_df['spacy-ingreds'][0]
print recipes_df[0][0]


# In[103]:


recipes_df['spacy-ingreds'].head()


# In[ ]:





# In[107]:


client.URL_SEARCH


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[108]:


client.URL_BASE


# In[109]:


client.URL_GET


# In[110]:


client.URL_META


# In[ ]:




