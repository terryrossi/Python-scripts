class Recipe(object):

  # Class Variable
  all_ingredients = []

  # Constructor
  def __init__(self, name):
    self.name = name
    self.ingredients = []
    self.cooking_time = 0
    self.calc_difficulty()

  # Getters and Setters  
  def set_name(self, name):
    self.name = name
  def get_name(self):
    return self.name
  
  def set_cooking_time(self, time):
    self.cooking_time = time
  def get_cooking_time(self):
    return self.cooking_time
  
  def get_difficulty(self):
     if self.difficulty == '':
        self.calc_difficulty()
     return self.difficulty

  #############################################################
  # Returns the list of ingredients
  def get_ingredients(self):
        return self.ingredients

  #############################################################
  # Search for an ingredient in the recipe
  def search_ingredient(self, ingredient):
     return ingredient in self.ingredients

  #############################################################
  # Method to add ingredients to the list of Ingredients of All Recipes
  def update_all_ingredients(self):
    for ingredient in self.ingredients:
        if ingredient not in Recipe.all_ingredients:
          Recipe.all_ingredients.append(ingredient)
    Recipe.all_ingredients.sort()

  #############################################################
  # Method to add ingredients to the recipe's list of ingredients
  def add_ingredients(self, ingredients): 
    
    for ingredient in ingredients:
        if ingredient not in self.ingredients:
            self.ingredients.append(ingredient)
    self.ingredients.sort()
    self.update_all_ingredients()
     
  
  #############################################################
  # function to Calculate the recipe difficulty:
  def calc_difficulty(self):
      
      nb_ingredients = len(self.ingredients)

      if (self.cooking_time < 10) and nb_ingredients < 4:
        self.difficulty = "Easy"
      elif (self.cooking_time< 10) and nb_ingredients >= 4:
        self.difficulty = "Medium"
      elif (self.cooking_time>= 10) and nb_ingredients < 4:
        self.difficulty = "Intermediate"
      elif (self.cooking_time >= 10) and nb_ingredients >= 4:
        self.difficulty = "Hard"


  ############################################################# 
  # Printing method
  def __str__(self):
      output = "\n--- Recipe --- \nName: " + str(self.name) + \
            "\nCooking Time: " + str(self.cooking_time) + \
             "\nDifficulty: " + str(self.difficulty) + \
             "\nIngredients of " + self.name + " : "
      for ingredient in self.ingredients:
        output = output + "\n" + str(ingredient)

      return output

  ############################################################# 
  # Printing method for all ingredients
  # This method should be a static Method as it involves several Recipe objects
  @staticmethod
  def list_all_ingredients():
    # Recipe.all_ingredients.sort()
    output = "\n\nIngredients of all Recipes: \n"
    for ingredient in Recipe.all_ingredients:
        output = output + "\n" + str(ingredient).capitalize()
    return output

  ############################################################# 
  # Search for recipes that contain aspecific ingredient
  # This method should be a static Method as it involves several Recipe objects
  @staticmethod
  def recipe_search(recipes, search_term):
     for recipe in recipes:
        if recipe.search_ingredient(search_term):
           print(recipe)


#####################################################################################
# Main Program
#####################################################################################
# Create tea Object
tea = Recipe("Tea")
tea.set_cooking_time(5)
ingredients= ["Tea Leaves", "Sugar", "Water"]
tea.add_ingredients(ingredients)
print(tea)

# test get_name and get_difficulty methods
print(f"The difficulty of {tea.get_name()} is {tea.get_difficulty()}")
print(f"There is sugar in Tea : {tea.search_ingredient('sugar')}")
print(f"There are potatoes in Tea : {tea.search_ingredient('potatoes')}")

# Create coffee Object
coffee = Recipe("Coffee")
coffee.set_cooking_time(4)
ingredients= ["Coffee Powder", "Sugar", "Water"]
coffee.add_ingredients(ingredients)
print(coffee)

# Create cake Object
cake = Recipe("Cake")
cake.set_cooking_time(50)
ingredients= ["Butter", "Sugar", "Eggs", "Milk", "Vanilla Essence", "Flour", "Baking Powder"]
cake.add_ingredients(ingredients)
print(cake)

# Create banana Object
banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.set_cooking_time(4)
ingredients= ["Bananas", "Sugar", "Water"]
banana_smoothie.add_ingredients(ingredients)
print(banana_smoothie)

# Print list of ingredients for All Recipes
print(Recipe.list_all_ingredients())

# Test Static method recipe_search for Water
search_term = "Water"
print(f"\nPrint all Recipes that contain: {search_term} .......")
recipe_list = [tea, coffee, cake, banana_smoothie]
Recipe.recipe_search(recipe_list, search_term)

# Test Static method recipe_search for Sugar
search_term = "Sugar"
print(f"\nPrint all Recipes that contain: {search_term} .......")
recipe_list = [tea, coffee, cake, banana_smoothie]
Recipe.recipe_search(recipe_list, search_term)

# Test Static method recipe_search for Bananas
search_term = "Bananas"
print(f"\nPrint all Recipes that contain: {search_term} .......")
recipe_list = [tea, coffee, cake, banana_smoothie]
Recipe.recipe_search(recipe_list, search_term)