import pickle

########################################################################
# The following function is meant for printing ingredients in the folowing format:
# Ingredients Available Across all Recipes : 
# ---------------------------------------- 
# INGREDIENT1
# INGREDIENT2
# ...

def display_ingredients(all_ingredients):
  print("")
  print("Ingredients Available Across all Recipes : ")
  print("---------------------------------------- ")

  # First we need to sort the list in alphabetic order
  all_ingredients.sort()

  # Then we loops over the list and print each ingredient capitalized with a sequential number
  for index, ingredient in enumerate(all_ingredients, start=1):
    print(f"{index} - {ingredient.capitalize()}")

########################################################################
# The following function is meant for printing recipes in the folowing format:
# ---- RECIPE -----
# Name: noodles
# Cooking_time: 33
# Ingredients :
# noodles
# butter
# cheese
# Difficulty: Intermediate

def display_recipes(recipes_list):
  for index, recipe in enumerate(recipes_list, start=1):
    print("")
    print(f"----- RECIPE {index} -----")
    print('')
    for key, value in recipe.items():
      if (key == "ingredients"):
        print("Ingredients : ")
        ingredients = list(value)
        for ingredient in ingredients:
          print(ingredient)
        continue
      
      print(f"{key.capitalize()}: {value}")

#########################################################################
# Open a file from user input 

def read_binary_file(filename):

  data = None

  try:
    with open(filename, 'rb') as file:    
      data = pickle.load(file)
      ############### Reading data from the binary file #################
      #### Data is supposed to be a dictionary containing two key-value pairs #####
      if isinstance(data, dict) and len(data) == 2:
        return data
      else:
        raise ValueError("File does not contain the expected format (list with two dictionaries)")
      
  except FileNotFoundError:
    print("File doesn't exist - Try again...")
    return None  
  except Exception as e:
    print('')
    print(f"An unexpected error occurred: {e}")
    return None
  
##########################################################################
# The following function search for all recipes in recipes_list that contain the ingredient
# passed as an argument
  
def search_recipe_with_ingredient(recipes_list, ingredient):
  found_recipes = [recipe for recipe in recipes_list if ingredient in recipe['ingredients']]
  return found_recipes

##########################################################################
# The following function is meant to search for an ingredient in the given data. The function takes in a dictionary called data as its argument. 
# The function will perform the following steps:
      # 1- shows the user all the available ingredients contained in data, under the key all_ingredients. 
      #         Each ingredient is displayed with a number
      # 2- Define a try block where the user gets to pick a number from this list. This number is used as the index to retrieve the corresponding ingredient, 
      #         which is then stored into a variable called ingredient_searched.
      # 3- Make an except clause that warns the user if the input is incorrect.
      # 4- Add an else clause that goes through every recipe in data (hint: recipes_list is the key that holds every recipe). 
      #         Each recipe that contains the given ingredient will be printed.

def search_ingredient(data):

  # unpack recipes_list and all_ingredients from data
  recipes_list, all_ingredients = data["recipes_list"], data["all_ingredients"] 

  # intitialize working variables
  ingredient_searched_num = 0
  ingredient_searched_str = ''
  found_recipes = []

# Check all_ingredients and if ok Show all ingredients in all_ingredients with index number
  if isinstance(all_ingredients, list) and len(all_ingredients) >= 0 :

    display_ingredients(all_ingredients)

# user gets to pick a number from the list of ingredients
  try: 
    print('')
    # ask ingredient number from user  
    ingredient_searched_num = int(input("Enter the index number of the ingredient you would like to search for : "))
   
    # Check validity of input from user 
    if 1 <= ingredient_searched_num <= len(all_ingredients):
      # find the ingredient assigned to the number (index = input number - 1)
      ingredient_searched_str = all_ingredients[ingredient_searched_num - 1]
      print('')
      print(f"You have selected : {ingredient_searched_str}")

      found_recipes = search_recipe_with_ingredient(recipes_list, ingredient_searched_str)
      
    else:
      print("")
      raise ValueError(f"Value must be between 1 and {len(all_ingredients)}")
      
  except ValueError as e:
    print(f"Invalid input: {e}")
    print('')
  finally:
    return found_recipes
      

##########################################################################
# Main Program
##########################################################################

# Working variables
default_look_for_ingredient = 'y'
look_for_ingredient = 'y'
default_filename = "myrecipes.bin"

# Ask user for name of binary file
print('')
user_input = input("Enter the filename for your recipes binary file (default : myrecipes.bin) : ")

# Check if the user input is not empty
if user_input.strip(): 
    filename = user_input
else:
    filename = default_filename

# Read binary file to gather existing recipes and ingredients
data = read_binary_file(filename)

# Check if returned data from binary file is of the appropriate format (dictionary with 2 lists)
if isinstance(data, dict) and len(data) == 2:
  
  while look_for_ingredient.lower() == 'y':
    # Look for recipes in recipes_list that contain a specific ingredient
    found_recipes = search_ingredient(data)
    
    # If there are any recipe matching the ingredient, then display them
    if len(found_recipes) >= 1:
      display_recipes(found_recipes)

    # Check if user wants to search for another ingredient
    user_input = input("Do you want to look for another ingredient? (Y/n)")

    # Check if the user input is not empty
    if user_input.strip():  # .strip() removes any leading/trailing whitespace
        look_for_ingredient = user_input
    else:
        look_for_ingredient = default_look_for_ingredient
 