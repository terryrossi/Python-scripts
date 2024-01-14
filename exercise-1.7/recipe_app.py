from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('mysql://cf-python:password@localhost/task_database')
# engine = create_engine('mysql://cf-python:password@localhost/task_database', echo=True)

Base = declarative_base()

class Recipe(Base):
    __tablename__ = 'final_recipes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    cooking_time = Column(Integer)
    ingredients = Column(String(255))
    difficulty = Column(String(20))
    
    all_ingredients = []  # Class variable to store all ingredients
    
    def __repr__(self):
        return "<Recipe(id, name='%s', difficulty='%s')>" % (
                             self.name, self.difficulty)
    
    def __str__(self):
        return f"\tRecipe ID: {self.id}\n" \
               f"\tRecipe Name: {self.name}\n" \
               f"\tCooking Time: {self.cooking_time} minutes\n" \
               f"\tDifficulty: {self.difficulty}\n" \
               f"\tIngredients: {self.ingredients}\n"
    
    def calc_difficulty(self):
        nb_ingredients = len(self.ingredients.split(', '))
       
        if (self.cooking_time < 10) and nb_ingredients < 4:
            self.difficulty = "Easy"
        elif (self.cooking_time < 10) and nb_ingredients >= 4:
            self.difficulty = "Medium"
        elif (self.cooking_time>= 10) and nb_ingredients < 4:
            self.difficulty = "Intermediate"
        elif (self.cooking_time >= 10) and nb_ingredients >= 4:
            self.difficulty = "Hard"

    def add_ingredients(self, ingredients):
        for ingredient in ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
        self.ingredients.sort()
        self.update_all_ingredients()

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)
        Recipe.all_ingredients.sort()

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def get_ingredients(self):
        return self.ingredients
    
    def return_ingredients_as_list():
        return Recipe.all_ingredients
    
    @property
    # To be able to call the method without the parentheses
    def list_ingredients(self):
        return self.ingredients.split(', ')

# Create the table
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Create a new recipe
def create_recipe():
    print("\nCreating a new recipe...")
    name = input("\nEnter the Name of the Recipe : ")
    while len(name) > 50 or not name.replace(" ", "").isalnum():
        print("\nInvalid name. Please enter a name with alphanumeric characters and maximum length of 50.")
        name = input("\nEnter the Name of the Recipe : ")
           
    cooking_time = input("\nEnter the Cooking Time : ")
    while not cooking_time.isnumeric():
        print("\nInvalid cooking time. Please enter a numeric value.")
        cooking_time = input("\nEnter the Cooking Time : ")
    cooking_time = int(cooking_time)

    ingredients = []
    add_ingredient = True
    while add_ingredient:
        ingredient = input("\nEnter an ingredient (type 'no' to finish): ")
        if ingredient.lower() == 'no':
            add_ingredient = False
        else:
            ingredients.append(ingredient.capitalize())  # Capitalize each ingredient

    new_recipe = Recipe(name=name, cooking_time=cooking_time, ingredients=', '.join(ingredients))  # Join ingredients with comma and space
    new_recipe.calc_difficulty()

    session.add(new_recipe)
    session.commit()
    print("\nRecipe added successfully.")

def view_all_recipes():
    recipes = session.query(Recipe).all()
    
    if not recipes:
        print("\nThere aren't any entries in the database.")
        return None
    
    for index, recipe in enumerate(recipes, start=1):
        print(f"\nRecipes : {index}")
        print("---------\n")
        print(recipe.__str__())

def search_by_ingredients():
    # Check if there are any entries in the table
    if session.query(Recipe).count() == 0:
        print("\nThere are no recipes in the database.")
        return

    # Retrieve ingredients from the table
    results = session.query(Recipe.ingredients).all()

    # Create a list of all ingredients
    all_ingredients = []
    for result in results:
        ingredients = result[0].split(', ')
        for ingredient in ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)

    # Display ingredients to the user
    print("\nAvailable ingredients:")
    print("----------------------")
    all_ingredients.sort()
    for i, ingredient in enumerate(all_ingredients):
        print(f"\t{i+1}. {ingredient}")

    # Ask user for ingredient selection
    selected_ingredients = input("\nEnter the numbers corresponding to the ingredients you'd like to search for (separated by commas): ")
    selected_ingredients = selected_ingredients.split(",")

    # Check if user's inputs match the options available
    for ingredient_num in selected_ingredients:
        if not ingredient_num.isdigit() or int(ingredient_num) < 1 or int(ingredient_num) > len(all_ingredients):
            print("\nInvalid ingredient selection.")
            return

    # Create a list of ingredients to search for
    search_ingredients = [all_ingredients[int(ingredient_num)-1] for ingredient_num in selected_ingredients]

    # Display the ingredients to search for
    print("\nSearching for recipes containing the following ingredients:\n")
    for ingredient in search_ingredients:
        print(f"\t{ingredient}")    

    # Create conditions for each ingredient to search for
    conditions = []
    for ingredient in search_ingredients:
        like_term = f"%{ingredient}%"
        conditions.append(Recipe.ingredients.like(like_term))

    # Retrieve recipes matching the search conditions
    recipes = session.query(Recipe).filter(*conditions).all()

    # Display the matching recipes
    print("\nMatching recipes:")
    print("----------------")
    for recipe in recipes:
        print(recipe.__str__())

def edit_recipe():
    # Check if there are any entries in the table
    if session.query(Recipe).count() == 0:
        print("\nThere are no recipes in the database.")
        return

    # Retrieve id and name for each recipe from the database
    results = session.query(Recipe.id, Recipe.name).all()

    # Display available recipes to the user
    print("\nAvailable recipes:")
    for result in results:
        print(f"{result[0]}. {result[1]}")

    # Ask user to pick a recipe by its id
    recipe_id = input("\nEnter the id of the recipe you'd like to edit: ")

    # Check if the chosen id exists
    if not session.query(Recipe).filter_by(id=recipe_id).first():
        print("\nInvalid recipe id.")
        return

    # Retrieve the recipe to edit from the database
    recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()

    # Display the recipe attributes to the user
    print("\nRecipe to edit : ")
    print("-----------------")
    print("\t1. Name:", recipe_to_edit.name)
    print("\t2. Ingredients:", recipe_to_edit.ingredients)
    print("\t3. Cooking Time:", recipe_to_edit.cooking_time)

    # Ask the user which attribute to edit
    attribute_num = input("\nEnter the number corresponding to the attribute you'd like to edit: ")

    # Check if the user's input is valid
    if attribute_num not in ['1', '2', '3']:
        print("\nInvalid attribute number.")
        return

    # Edit the respective attribute based on the user's input
    if attribute_num == '1':
        new_name = input("\nEnter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute_num == '2':
        new_ingredients = input("\nEnter the new ingredients (comma separated): ")
        new_ingredients = new_ingredients.split(",")
        new_ingredients = [ingredient.strip() for ingredient in new_ingredients]
        new_ingredients = ', '.join(new_ingredients)
        concatenated_ingredients = recipe_to_edit.ingredients + ', ' + new_ingredients
        recipe_to_edit.ingredients = concatenated_ingredients
    elif attribute_num == '3':
        new_cooking_time = int(input("\nEnter the new cooking time: "))
        recipe_to_edit.cooking_time = new_cooking_time

    # Recalculate the difficulty
    recipe_to_edit.calc_difficulty()

    # Commit the changes to the database
    session.commit()

def delete_recipe():
    # Check if there are any entries in the table
    if session.query(Recipe).count() == 0:
        print("\nNo recipes found in the database.")
        return

    # Retrieve the id and name of every recipe in the database
    recipes = session.query(Recipe.id,Recipe.name).all()

    # List the recipes for the user to choose from
    print("\nAvailable Recipes:")
    for recipe in recipes:
        print(f"Id: {recipe.id}, Name: {recipe.name}")

    # Ask the user for the id of the recipe to delete
    recipe_id = int(input("\nEnter the id of the recipe you want to delete: "))

    # Verify the input
    recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()
    if recipe_to_delete is None:
        print("\nInvalid recipe id.")
        return

    # Ask for confirmation
    confirmation = input(f"\nAre you sure you want to delete the recipe '{recipe_to_delete.name}'? (y/N): ")
    if confirmation.lower() != "y":
        print("\nDeletion canceled.")
        return

    # Perform the delete operation and commit the change
    session.delete(recipe_to_delete)
    session.commit()

    print("\nRecipe deleted successfully.")


############################################################################################################
# Main program
############################################################################################################
    
while True:
    print("\nMain Menu:")
    print("----------")
    print("\n\t1. Create a new recipe")
    print("\t2. View all recipes")
    print("\t3. Search for recipes by ingredients")
    print("\t4. Edit a recipe")
    print("\t5. Delete a recipe")
    print("\nType 'quit' to quit the application")

    user_choice = input("\nEnter your choice: ")

    if user_choice == "1":
        create_recipe()
    elif user_choice == "2":
        view_all_recipes()
    elif user_choice == "3":
        search_by_ingredients()
    elif user_choice == "4":
        edit_recipe()
    elif user_choice == "5":
        delete_recipe()
    elif user_choice.lower() == "quit":
        session.close()
        engine.dispose()
        break
    else:
        print("\nInvalid input. Please try again.")
