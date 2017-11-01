**Specification**
 
Splash screen [optional]

[comment]: # (Can you use Country/World food pics from presentation in the app - with attribution)   

**Summary**

Just Eat It: the Friendly Food Finder app - empowering those with food allergies to move confidently 
through their world.

**Motivation**

While travelling, here or overseas, food provides a window into other cultures and peoples.
The simple act of sharing a meal promotes understanding and acceptance.

However, if like my son you have food allergies, travelling and finding friendly foods can be difficult 
and sometimes life-threatening!

Food allergies are:
1. Common
2. Increasing in frequency
3. Have a serious impact
4. Are socially isolating
5. Are a significant cost

Thus, for my Capstone project, I have developed an app which allow a user to specify their allergy profile, 
combined with recipe data from Yummly to produce TripAdvisor-like personalised recommendations.

**Allergy Profiles**

[comment]: (https://www.fda.gov/food/resourcesforyou/consumers/ucm079311.htm)

The eight foods identified by the FDA are:

* Milk
* Eggs
* Fish (e.g., bass, flounder, cod)
* Crustacean shellfish (e.g., crab, lobster, shrimp)
* Tree nuts (e.g., almonds, walnuts, pecans)
* Peanuts
* Wheat
* Soybeans

**Functionality**

For a users’ specific food allergies it will  Answering questions like:

* Where is it mostly likely in the world/country/region that I can eat?
* If I relax one of my allergens (e.g. allowing for something to be on the side) how does this change/improve this picture? 

The app also allows you to register allergy profile & demographics to contribute to a (de-identified) 
crowd-sourced research database to potentially provide researchers with more definitive data than 
available with survey-based approaches.

The techniques and tools that I have used to develop the app are:

Techniques:    NLP, MCA (PCA)

Tools:
    Yummly, Pandas, SQLite, spaCy
    Flask -SQLAlchemy, -WTF, -Login



Just  Eat  It : Friendly-Food Finder
* Context
    * Sharing meals is a key to accessing and understanding others and their cultures
    * 1 in 10 people throughout the world have a food allergy
* App to assist those with dietary restrictions to make informed menu choices
* Version 1: Initially targeted at those, like my son who have food allergies, for whom these decisions can literally be a matter of life and death
* Being “excluded” from the table when you already have dietary restrictions compounds the problem
* Aiming for inclusion and integration via confidence to know what to order or how to make simple adjustments to recipes to put them back "on the table”
* Currently investigation more sophisticated analysis and features
* Equally applies to other dietary restriction profiles - Health, Wellness, Belief or other Preference (some people just don’t like broccoli!) ==> Version 2
* Version 3 => Standardisation whereby data is self-contributed by restaurants to know the precise ingredients to provide more precision to the recommendations

Achievements so far:

* Adapted the milestone project 
* Signed-up for Hackathon access to use the Yummly API
* Located and installed a Python wrapper (import yummly)
* Successfully returned data from a prototype query
* Local prototype for the app adapted from Milestone app

Key next steps:

* DATA
    * Download and save a sub-sample of data/queries (framework for this e.g. dill?)
        * Yes - think I’ll start with Dill and Pandas - then scale 
    * Understand the capabilities and limitations of the Yummly API and caching
    * Include other potential datasets:
        * e.g. https://developers.delivery.com
        * e.g. http://www.brewerydb.com
        * e.g. https://developer.nutritionix.com/docs/v2  (has a NLP for ingredients!!!)
* SCIENCE
    * Perform EDA on a subset of Yummly data
    * Investigate the analytical possibilities
    * Consider the PCA-equivalents for textual data and look at “Eigen-Ingredients”
* APP
    * Map out the core functionality of the app
    * Imagine the design (look + feel) of the app
* TECH
    * Sort out seamless deployment to Heroku (still a few heuristics required!)
    * Heroku - look at their automated deployment options:
        * https://devcenter.heroku.com/articles/pipelines
        * See the Docker/Flask example - https://github.com/heroku-examples/python-miniconda


**TDI Pre-course feedback**

[comment]: # (TODO: Address this feedback)

Great idea. 

A proposal for an app: for the top 10 allergies / dietary restrictions, 
give the top 10 items of a cuisine that conform to those restrictions. 
e.g. What do you eat in a Thai restaurant if your'e allergic to peanuts?

*TripAdvisor plus Yummly = > ANAGRAM =>   Simply Avoid Surly Trump* 