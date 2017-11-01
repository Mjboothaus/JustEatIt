# **Allergy Profiles**
#
# [comment]: (https://www.fda.gov/food/resourcesforyou/consumers/ucm079311.htm)
#
# The eight foods identified by the FDA are:
#
# * Milk
# * Eggs
# * Fish (e.g., bass, flounder, cod)
# * Crustacean shellfish (e.g., crab, lobster, shrimp)
# * Tree nuts (e.g., almonds, walnuts, pecans)
# * Peanuts
# * Wheat
# * Soybeans

common_food_allergens_no_seafood = ['milk', 'egg', 'peanut']

top_food_allergen_profiles = [['milk'], ['egg'], ['peanut'], ['milk', 'egg'], ['milk', 'peanut'], ['egg', 'peanut']]

for i, ingredient_list in enumerate(top_food_allergen_profiles):
    print i+1, ingredient_list