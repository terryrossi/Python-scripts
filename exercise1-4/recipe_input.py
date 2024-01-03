import pickle

# List of recipes
recipes_list = []
# List of ingredients
all_ingredients = []
# Indicates if user wants to add a new recipe
more_recipes = "y"
# Indicates if a new recipe has been added
new_recipe_to_add = "n"
# indiates if a new ingredient has been added
new_ingredient_to_add = "n"

#############################################################
 # function to Calculate the recipe difficulty:

def calc_difficulty(recipe):
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

#############################################################
# Function receiving input from user to create a recipe
# ... as the user inputs ingredients, the function also adds NEWingredients to all_ingredients

def create_recipe():
  
  # Working variables
  default_more_ingredients = "y" # Used to keep on asking for more ingredients
  more_ingredients = "y" # Used to keep on asking for more ingredients
  ingredients = []       # List of ingredients to create the new recipe

  print('')
  name = input("Enter the Name of the Recipe : ")
  print('')
  cooking_time = int(input("Enter the Cooking Time : "))

  while more_ingredients.lower() == "y":  # While loop to keep adding more ingredients
    print('')
    ingredient = input("Enter an ingredient : ")

    if (ingredient not in ingredients):   # Condition to check for duplicate ingredients
      ingredients.append(ingredient)

    if (ingredient not in all_ingredients):   # If the ingredient is not yet in the all_ingredients...
      # ... Add the ingredient to the all_ingredients
      all_ingredients.append(ingredient)

    print('')
    user_input = input("More ingredients? (Y/n) : ") # Ask he user if he/she wants to add more ingredients

    # Check if the user input is not empty
    if user_input.strip():  # .strip() removes any leading/trailing whitespace
        more_ingredients = user_input
    else:
        more_ingredients = default_more_ingredients

  # Creates the new recipe
  recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}
  
  # Calculate recipe difficulty
  calc_difficulty(recipe)

  # Returns the new recipe 
  return recipe

#########################################################################
# Open a file from user input 

def read_binary_file(filename):

  data = None

  try:
      with open(filename, 'rb') as file:    
        data = pickle.load(file)
        ############### Process data from the binary file #################
        #### Data is supposed to be a dictionary containing two key-value pairs #####
        if isinstance(data, dict) and len(data) == 2:
          return data["recipes_list"], data["all_ingredients"]  # Assuming the file has exactly two lists
        else:
          raise ValueError("File does not contain the expected format (list with two dictionaries)")
       
  except FileNotFoundError:
      print("")
      create_new_file = input("File doesn't exist - Would you like to create it? (y/n) : ")
      if create_new_file:
         
        with open(filename, 'wb') as file:
          pass
        return [], []    
  except Exception as e:
        print('')
        print(f"An unexpected error occurred: {e}")
        return [], [] 
      
  return [], []

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

def display_recipes():
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

##########################################################################
# The following function is meant for printing ingredients in the folowing format:
# Ingredients Available Across all Recipes : 
# ---------------------------------------- 
# INGREDIENT1
# INGREDIENT2
# ...

def display_ingredients():
  print("")
  print("Ingredients Available Across all Recipes : ")
  print("---------------------------------------- ")

  # First we need to sort the list in alphabetic order
  all_ingredients.sort()

  # Then we loops over the list and print each ingredient capitalized
  for ingredient in all_ingredients:
    print(ingredient.capitalize())
   

#################################################################
# write/add new recipes and ingredients in binary file
    
def write_to_binary_file(filename):
  data = {"recipes_list" : recipes_list, "all_ingredients" : all_ingredients}
  try:
    with open(filename, 'wb') as file:    
        pickle.dump(data, file)
        
  except FileNotFoundError:
      print('')
      print("Filename doesn't exist - exiting.")
  except Exception as e:
        print('')
        print(f"An unexpected error occurred: {e}")
      
  return [], []
  
################################################################
# Main Program
################################################################

# Working variables
default_more_recipes= 'y'
default_filename = "myrecipes.bin"

# Ask user for name of binary file
print('')
user_input = input("Enter the filename for your recipes binary file (Default : myrecipes.bin) : ")

# Check if the user input is not empty
if user_input.strip(): 
    filename = user_input
else:
    filename = default_filename

# Process binary file to gather existing recipes and ingredients
recipes_list, all_ingredients = read_binary_file(filename)

# display the returned recipes and ingredients
if isinstance(recipes_list, list) and len(recipes_list) >= 0 :
    print('')
    print("Data already on file: ")
    print("--------------------- ")

    display_recipes()

if isinstance(all_ingredients, list) and len(all_ingredients) >= 0 :

    display_ingredients()

# Create or add recipes from the user input 
print('')
user_input = input("Would you like to add a Recipe? (Y/n) : ") # Ask he user if he/she wants to add another recipe
# Check if the user input is not empty
if user_input.strip():  # .strip() removes any leading/trailing whitespace
  more_recipes = user_input
else:
  more_recipes = default_more_recipes

while more_recipes.lower() == 'y': # While loop to keep adding more recipes
  new_recipe_to_add = "y" # indicates that at least 1 new recipe has been added to the list
  new_ingredient_to_add = "y" # indicates that at least 1 new ingredients has been added to the list
  recipe = create_recipe() # Call to the function that creates a new recipe
  recipes_list.append(recipe) # add the new recipe to the recipes_list
  print('')
  user_input = input("Another Recipe? (Y/n) : ") # Ask he user if he/she wants to add another recipe

   # Check if the user input is not empty
  if user_input.strip():  # .strip() removes any leading/trailing whitespace
    more_recipes = user_input
  else:
    more_recipes = default_more_recipes

# if a new recipe or ingredient has been added, we need to re-write the binary file
# In reality, we should find a different format for the files so we can add new data without having 
# to re-write the file which is a total waste of ressources.
if new_recipe_to_add.lower() == 'y' or new_ingredient_to_add.lower() == 'y':
   
  write_to_binary_file(filename)
  print('')
  print("Updated Data: ")
  print("------------- ")
else:
  print('')
  print("NO NEW DATA - Previous Data: ")
  print("---------------------------- ")

# before ending the program, let's show the user the final lists:
  
display_recipes()
display_ingredients()


