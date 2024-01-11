
import mysql.connector

from mysql.connector import Error

#######################################################################################
# SQL Function initiating Database Connection
def initiate_database_connection():
  # Open Connection to MySQL
  try:

    conn = mysql.connector.connect(
      host = 'localhost',
      user = 'cf-python',
      passwd='password'
    )

    if conn.is_connected():
      print("\nConnection successful!")

    # Initialize a cursor
    cursor = conn.cursor()

    # Create a database called task_database
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

    # Open the Database
    cursor.execute('USE task_database')

    # Create the table Recipes
    cursor.execute('''CREATE TABLE IF NOT EXISTS Recipes(
        id             INT PRIMARY KEY AUTO_INCREMENT,
        name           VARCHAR(50),
        ingredients    VARCHAR(255),
        cooking_time   SMALLINT,
        difficulty     VARCHAR(20), 
        CHECK (difficulty IN ('easy', 'medium', 'intermediate','hard')) 
    )''')

  except Error as e:
    print(f"Error connecting to MySQL: {e}")

  except Exception as e:
    print(f"An unexpected error occurred: {e}")

  finally:

    # Checking Creation of table
    # print('\nRecipes Table DDL :\n')
    # cursor.execute('DESCRIBE Recipes')

    # result = cursor.fetchall()
    # for row in result:
    #   print(row)

    return conn, cursor
  
#############################################################
# SQL Function to create a list of ingredients
def sql_select_ingredients(cursor):

  cursor.execute('SELECT ingredients FROM Recipes')

  all_ingredients = []
  results = cursor.fetchall()
  
  for ingredients_string in results:
     
      ingredients_list = ingredients_string[0].split(', ')
      
      for ingredient in ingredients_list:
        if ingredient not in all_ingredients:
          all_ingredients.append(ingredient)
  return all_ingredients    

#################################################################################
# SQL Function to insert a new recipe in the DB
def sql_insert_new_recipe(cursor, recipe):

  name = recipe["name"]
  cooking_time = recipe["cooking_time"]
  ingredients = ', '.join(recipe["ingredients"])  # Convert list of ingredients to string
  difficulty = recipe["difficulty"]
 
  # Creating the insert statement
  try: 
    sql = 'INSERT INTO Recipes (name, cooking_time, ingredients, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, cooking_time, ingredients, difficulty)
    cursor.execute(sql, val)

  except Error as e:
    print(f"Error connecting to MySQL: {e}")
  except Exception as e:
    print(f"An unexpected error occurred: {e}")

  finally:
     print(f'\nRecipe {name} has been created ! \n')


#################################################################################
# SQL Function to UPDATE a recipe in the DB
def sql_update_recipe(cursor, query, new_value,search_term ):

  try:
      cursor.execute(query, (new_value, search_term))

  except Exception as e: # In case of SQL Error
      print(f"An unexpected error occurred: {e}")
      return

#################################################################################
# SQL Function to DELETE a recipe in the DB
def sql_delete_recipe(cursor, query, search_term ):

  try:
      cursor.execute(query,(search_term,))

  except Exception as e: # In case of SQL Error
      print(f"An unexpected error occurred: {e}")
      return

#############################################################
# Function to display the list of ingredients
def display_ingredients(all_ingredients):

  for index, ingredient in enumerate(all_ingredients,start=1):
    print(f'{index} - {ingredient.capitalize()}')

#############################################################
# Function for the user to select an ingredient
def pick_an_ingredient(all_ingredients):
    while True:
      ingredient_index = input('\nPlease Enter the id of the ingredient you would like to Select : ')

      try:
        ingredient_index = int(ingredient_index)
        if 1 <= ingredient_index <= len(all_ingredients):
          break
        else:
          print(f'\nNumber must be between 1 and {len(all_ingredients)}')

      except ValueError:
        print(f'\nPlease enter a Valid number between 1 and {len(all_ingredients)}')
    
    return all_ingredients[int(ingredient_index)-1]

#############################################################
# Function for the user to select a column to update
def pick_a_column(): 
        columns_list = ['name', 'cooking_time', 'ingredients']
        print('\n  Columns to choose from : ')
        for i, col in enumerate(columns_list, 1):
            print(f'     {i} - {col}')

        # Ask the user to select a column
        while True:
          column_number = input("\nPlease enter the number of the Column you would like to update : ")

          try:
            column_number = int(column_number)
            # Check validity of user entry
            if column_number in [1, 2, 3]:   
                break
            else:
              print(f'\nNumber must be between 1 and 3')
          except ValueError:
            print(f'\nPlease enter a Valid number between 1 and 3')

        return columns_list[column_number-1]  


#############################################################
 # function to Calculate the recipe difficulty of the new Recipe Object (dictionary):

def calc_difficulty_object(recipe):
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
    return recipe

#############################################################
 # function to Update the recipe difficulty on an SQL queried Recipe (tuple)

def update_difficulty(cooking_time, ingredients):
    
    nb_ingredients = len(ingredients.split(', '))

    if (cooking_time < 10) and nb_ingredients < 4:
      difficulty = "Easy"
    elif (cooking_time < 10) and nb_ingredients >= 4:
      difficulty = "Medium"
    elif (cooking_time >= 10) and nb_ingredients < 4:
      difficulty = "Intermediate"
    elif (cooking_time >= 10) and nb_ingredients >= 4:
      difficulty = "Hard"
    return difficulty



###########################################################################
# Function to create a recipe Object that will be used to insert in the DB

def create_recipe_object():
  
  # Working variables
  default_more_ingredients = "y" # Used to keep on asking for more ingredients
  more_ingredients = "y" # Used to keep on asking for more ingredients
  ingredients = []       # List of ingredients to create the new recipe

  while True:
      name = input("\nEnter the Name of the Recipe : ")
      if name:
        break
      else:
        print("\nPlease enter a valid name")

  while True:
    try: 
      cooking_time = int(input("\nEnter the Cooking Time : "))
      break
    except ValueError:
      print('\nPlease enter a valid number')

  while more_ingredients.lower() == "y":  # While loop to keep adding more ingredients
    
    ingredient = input("\nEnter an ingredient : ")

    if (ingredient not in ingredients):   # Condition to check for duplicate ingredients
      ingredients.append(ingredient)

    user_input = input("\nMore ingredients? (Y/n) : ") # Ask he user if he/she wants to add more ingredients

    # Allow user to press enter for Y as a default
    if user_input.strip():  # .strip() removes any leading/trailing whitespace
        more_ingredients = user_input
    else:
        more_ingredients = default_more_ingredients

  # Creates the new recipe object
  recipe = {"name": name, "cooking_time": cooking_time, "ingredients": ingredients}
  
  # Calculate recipe difficulty
  recipe = calc_difficulty_object(recipe)

  # Returns the new recipe 
  return recipe

###########################################################################
# Function to allow the user to select a Recipe
def select_a_recipe():
    query = 'SELECT id, name, cooking_time, ingredients, difficulty FROM Recipes'
    message = "\nHere are your Recipes"
    display_recipes(cursor, query, '', message)

    # Second: Ask the user to choose the recipe to update and prepare to fetch it in the DB 
    search_term = ''
    while True:
      recipe_id = input('\nPlease Enter the id of the Recipe you would like to Select : ')
      try: 
        search_term = int(recipe_id)
        break
      except ValueError:
        print(f'\nPlease enter a Valid number')
         
    query = 'SELECT id, name, cooking_time, ingredients, difficulty FROM Recipes WHERE id=%s'
    cursor.execute(query, (search_term,))

    # fetch the recipe
    recipe = cursor.fetchall()

    # In case of an issue fetching the recipe
    if not recipe:
        print(f'\nNo recipe found with id : {recipe_id} ')
        return
    
    return recipe

###########################################################################
# Function to allow the user to Add or Remove an ingredient
def process_ingredients_update(ingredients_list):
    
    response_default = 'A'
    response = ''
    while response not in ['A','a','R','r']:
        response = input('\nWould you like to Add or Remove an Ingredient? (A/r) : ')
        if not response:
           response = response_default

    if response in ['A', 'a']:
      new_ingredient = input('\nPlease enter the new ingredient : ')
      if (new_ingredient not in ingredients_list):   # Condition to check for duplicate ingredients
        ingredients_list.append(new_ingredient)
      else:
        print('\nIngredient already in the list!\n')
    elif response in ['R','r']:

       # Display the list of Ingredients
      print('\nList of ingredients : ')
      print('---------------------')
      display_ingredients(ingredients_list)

      ingredient_to_remove = pick_an_ingredient(ingredients_list)

      ingredients_list.remove(ingredient_to_remove)
    ingredients_string = ', '.join(ingredients_list)  # Convert list of ingredients to string

    return ingredients_string
    

###################################################################################
# The Following methods are the ones called from the main menu based on user input
###################################################################################
# 1. List all recipes

def display_recipes(cursor,query, search_term, message):
    
    if search_term:
      cursor.execute(query, (search_term,))
    else:
      cursor.execute(query)

    recipes = cursor.fetchall()
    print(message)
    for index, recipe in enumerate(recipes,start=1):
      print('\nRecipe ',index)
      print("---------")
      print('  Id : ', recipe[0])
      print('  Name : ',recipe[1].capitalize())
      print('  Cooking Time : ',recipe[2])
      print('  Difficulty : ', recipe[4])
      ingredients_string = recipe[3]
      ingredients_list = ingredients_string.split(', ')
      ingredients_list.sort()
      print('  Ingredients : ')
      for ingredient in ingredients_list:
        print('     ',ingredient.capitalize())
      

#################################################################################
# 2. Create a new recipe
        
def create_recipe(cursor):

  # First create a recipe object 
  recipe = create_recipe_object()
  # Then insert the new object in the DB
  sql_insert_new_recipe(cursor, recipe)


######################################################################
# 3. Search for a recipe by ingredient
  
def search_recipe(cursor):

  # First: Create a list of ingredients
  all_ingredients = sql_select_ingredients(cursor)

  # Second: Display the list of all Ingredients with an index next to each item
  all_ingredients.sort()
  print('\nList of ingredients : ')
  print('---------------------')
  display_ingredients(all_ingredients)

  # Third Ask user to select one of the ingredients and check entry
  ingredient_selected = pick_an_ingredient(all_ingredients)

  # Finally: Search and display Recipes that contain the selected ingredient
  # Prepare the query for the display_recipes function
  query = (f'SELECT id, name, cooking_time, ingredients, difficulty FROM Recipes WHERE ingredients LIKE %s')
  search_term = '%' + ingredient_selected + '%'
  message = f"\nHere are your Recipes containing : {ingredient_selected.capitalize()}"
  display_recipes(cursor, query, search_term, message)

######################################################################
# 4. Update an existing recipe

def update_recipe(cursor):
    # First: Allow user to select a recipe
    recipe = select_a_recipe()
    # Unpack Recipe
    id, name, cooking_time, ingredients, difficulty = recipe[0]

    ##### (Print the selected Recipe for testing) ######
    print('\nRecipe selected :')
    print('----------------- ')
    print('id : ', id)
    print('Name ; ', name.capitalize())
    print('Cooking Time : ', cooking_time)
    ingredients_list = ingredients.split(', ')
    ingredients_list.sort()
    
    for ingredient in ingredients_list:
        print('     ',ingredient.capitalize())
    print('Difficulty ; ', difficulty)

    # Second: Allow user to select a column to update
    column_picked = pick_a_column()
    
    # Ask user to enter new value and check for validity of entry
    new_value = ''

    if column_picked == 'cooking_time': # Check for cooking_time column
        while True:
          new_value = input(f'\nEnter the new value for {column_picked}: ')
          # Value entered must be numeric
          try:
            new_value = int(new_value)
            break
          except ValueError:
            print(f'\nPlease enter a Valid number')
        cooking_time = new_value

    elif column_picked == 'ingredients': # Check for Ingredients column

      # recreate the list of ingredients from the string
      ingredients_list = ingredients.split(', ') 

      # Update the list of ingredients
      ingredients_list.sort()
      ingredients = process_ingredients_update(ingredients_list)

      new_value = ingredients

    # check for Name column
    elif column_picked == 'name':  # Check for name column
        
        new_value = input(f'\nEnter the new value for {column_picked}: ')      

    # Prepare and execute SQL Update in the DB
    query = f'UPDATE Recipes SET {column_picked} = %s WHERE id = %s'
    sql_update_recipe(cursor, query, new_value,id )

    # Update difficulty in the DB
    updated_difficulty = update_difficulty(cooking_time, ingredients)

     # Prepare and execute SQL Update difficulty in the DB
    query = f'UPDATE Recipes SET difficulty = %s WHERE id = %s'
    sql_update_recipe(cursor, query, updated_difficulty,id )
      
    # Display the updated recipe
    query = 'SELECT id, name, cooking_time, ingredients, difficulty FROM Recipes WHERE id=%s'
    message = '\nHere is your Updated Recipe : '
    display_recipes(cursor, query, id, message)


######################################################################
# 5. Delete a recipe
    
def delete_recipe(cursor):

  # First: Allow user to select a recipe
  recipe = select_a_recipe()

  if recipe: 

    delete = ''
    delete_default = 'n'

    print('\nYou have selected : ', recipe[0][1])

    while delete not in ['Y','y','n','N']:
      delete = input('\nDo you want to DELETE this Recipe? (y/N) : ')
      if not delete:
        delete = delete_default

    if delete in ['Y','y']:
      query='DELETE FROM Recipes WHERE id=%s'
      search_term = recipe[0][0]
      sql_delete_recipe(cursor, query, search_term)
      print(f'\nRecipe {recipe[0][1]} has been Deleted!!!\n')

  # return None


######################################################################
# Display the Main Menu

def main_menu(conn, cursor):
  exit_menu = ''

  while exit_menu.lower() != 'exit':

    print('\nMain Menu')
    print('=========================================')
    print('Pick a choice : ')
    print('1. List all recipes')
    print('2. Create a new recipe')
    print('3. Search for a recipe by ingredient')
    print('4. Update an existing recipe')
    print('5. Delete a recipe')
    exit_menu = input('\nEnter a choice between 1-4 or "exit" to exit : ')

    if exit_menu== '1':

      # Display All Recipes
      query = 'SELECT id, name, cooking_time, ingredients, difficulty FROM Recipes'
      message = "\nHere are your Recipes : "
      display_recipes(cursor, query, '', message)

    elif exit_menu == '2':
      create_recipe(cursor)
    elif exit_menu == '3':
      search_recipe(cursor)
    elif exit_menu == '4':
      update_recipe(cursor)
    elif exit_menu== '5':
      delete_recipe(cursor)
    
    else:
      print('\nPlease enter a valid number')
    # Commit Changes
    if exit_menu in['2','4','5']:
      print('\nChanges committed!!\n')
      conn.commit()
  # Close cursor and connection
  cursor.close()
  conn.close()

######################################################################
# Main Program
######################################################################

conn, cursor = initiate_database_connection()

main_menu(conn, cursor)


