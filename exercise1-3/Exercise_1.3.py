recipes_list = []
ingredients_list = []
more_recipes = "y"

print(recipes_list,ingredients_list)

# Function receiving input from user to create a recipe
# ... as the user inputs ingredients, the function also adds NEWingredients to ingredients_list
def take_recipe():
  
  more_ingredients = "y" # Used to keep on asking for more ingredients
  ingredients = []       # List of ingredients to create the new recipe

  name = input("Enter the Name of the Recipe : ")
  cooking_time = int(input("Enter the Cooking Time : "))

  while more_ingredients.lower() == "y":  # While loop to keep adding more ingredients
    ingredient = input("Enter an ingredient : ")

    if (ingredient not in ingredients):   # Condition to check for duplicate ingredients
      ingredients.append(ingredient)

    if (ingredient not in ingredients_list):   # If the ingredient is not yet in the ingredients_list...
      # ... Add the ingredient to the ingredients_list
      ingredients_list.append(ingredient)

    more_ingredients = input("More ingredients? (y/n) : ") # Ask he user if he/she wants to add more ingredients

  # Creates the new recipe
  recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}
  
  # Returns the new recipe 
  return recipe


while more_recipes.lower() == 'y': # While loop to keep adding more recipes

  recipe = take_recipe() # Call to the function that creates a new recipe

  # Calculate the recipe difficulty:
  cooking_time = recipe["cooking_time"]
  nb_ingredients = len(recipe["ingredients"])

  if (cooking_time < 10) and nb_ingredients < 4:
    recipe["difficulty"] = "Easy"
  elif (cooking_time < 10) and nb_ingredients >= 4:
    recipe["difficulty"] = "Medium"
  elif (cooking_time >= 10) and nb_ingredients < 4:
    recipe["difficulty"] = "Intermediate"
  elif (cooking_time >= 10) and nb_ingredients >= 4:
    recipe["difficulty"] = "Hard"

  recipes_list.append(recipe) # add the new recipe to the recipes_list

  more_recipes = input("Another Recipe? (y/n) : ") # Ask he user if he/she wants to add another recipe


# The following loop is meant for printing recipes in the folowing format:
# REIPE :
# Name: noodles
# Cooking_time: 33
# Ingredients :
# noodles
# butter
# cheese
# Difficulty: Intermediate

for recipe in recipes_list:
  print("")
  print("RECIPE :")
  for key, value in recipe.items():
    if (key == "ingredients"):
      print("Ingredients : ")
      ingredients = list(value)
      for ingredient in ingredients:
        print(ingredient)
      continue
    
    print(f"{key.capitalize()}: {value}")


# The following loop is meant for printing ingredients in the folowing format:
print("")
print("Ingredients Available Across all Recipes : ")
print("---------------------------------------- ")

# First we need to sort the list in alphabetic order
ingredients_list.sort()

# Then we loops over the list and print each ingredient capitalized
for ingredient in ingredients_list:
  print(ingredient.capitalize())