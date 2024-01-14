# Python-ORM Exercise 1.7

## Part 1: Set Up the Script & SQLAlchemy

### Directions

1. Open a script file called `recipe_app.py`.

2. As we saw earlier, the application requires a number of packages and functions for each part to operate, such as model definitions and session creation. Make sure we import all the packages and methods necessary to build the application.

3. Set up SQLAlchemy if you haven’t already. Make sure that the MySQL server is up and running. Take note of the username, password, hostname, and database name.

4. Use the credentials and details above to create an engine object called `engine` that connects to the desired database. (Note: You can use the database `task_database` that you created in the previous Exercise.)

5. Make the session object that you’ll use to make changes to the database. To do this, generate the `Session` class, `bind` it to the `engine`, and initialize the `session` object.

```from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

engine = create_engine('mysql://cf-python:password@localhost/task_database')

Base = declarative_base()

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
```

## Part 2: Create the Model and Table

Store the declarative base class into a variable called Base. Then, begin the definition for the Recipe model.

### Directions:

1. The `Recipe` class should inherit the `Base` class that we created earlier.

2. Define an attribute to set the table’s name as `final_recipes`.

3. Define these attributes to create columns in the table:

   - `id`: integer; primary key; increments itself automatically.
   - `name`: string with 50-character limit; stores the recipe’s name.
   - `ingredients`: string type; character limit of 255; stores the ingredients of the recipe in the form of a string.
   - `cooking_time`: integer; stores the recipe’s cooking time in minutes
   - `difficulty`: string with 20-character limit; stores one of four strings that describe the difficulty of the recipe (`Easy`, `Medium`, `Intermediate`, and `Hard`).

4. Define a `__repr__` method that shows a quick representation of the recipe, including the `id`, `name`, and `difficulty`.

5. Define a `__str__` method that prints a well-formatted version of the recipe. Get creative with the print statements! Some quick tips:

   - The `\t` characters create a tab space, which is equivalent to 4 spaces.
   - The `\n` characters string creates a new line. (Remember: these characters are strings, so they’ll always go inside quotation marks.)
   - To repeat a set of characters multiple times, simply type the desired characters in double quotes, followed by `*(<number of times to be repeated>)`. For example, typing in `print("-"*5)` would give `-----`.
   - Use the `end` keyword argument in the `print()` function to explicitly define what comes after its output. By default, every `print()` statement creates a new line.

   Example :
   `print("Hello, end="-")
print("World")`
   Gives: `Hello-World`

6. Define a method called `calculate_difficulty()` to calculate the difficulty of a recipe based on the number of `ingredients` and `cooking time`. We may copy the same code from the task in the previous Exercise here, with the exception of the last step (where instead of returning the calculated difficulty, the difficulty level is instead assigned to the instance variable `self.difficulty`).

7. Define a method that retrieves the `ingredients` string inside the Recipe object as a `list`, called `return_ingredients_as_list()`. It will follow these steps:

   - If the instance variable `self.ingredients` is an empty string, return an empty list.
   - Otherwise, use the `split()` method available to strings to split the string into a list wherever there’s a comma followed by a space `(,)`. Return this list.

8. Once we’re done defining the model, create the corresponding table on the database using the `create_all()` method from `Base.metadata`.

## Part 3: Define the Main Operations as Functions

Before creating the main menu, we need to establish the functions that get executed when an option on the main menu is picked. Let’s go through the five functions, one by one.

### Function 1: create_recipe()

1. Collect the details of the recipe (`name`, `ingredients`, `cooking_time`) from the user.

2. Ensure all the inputs are appropriate (e.g., `name` doesn’t extend past 50 characters, or `cooking_time` isn’t a letter of the alphabet). Use the following methods to perform these checks for a given string called `line`:

   - `len()` - use `len(line)` to get the length of `line` as an integer.
   - `isalnum()` - `line.isalnum()` gives `True` or `False` based on whether `line` contains alphanumeric characters.
   - `isnumeric()` - `line.isnumeric()` returns `True` or `False` based on whether line contains only numbers.
   - `isalpha()` - `line.isalpha()` returns `True` or `False` based on whether line contains only alphabetical characters.

3. Collect the ingredients from the user in the following manner:

   - Define a temporary empty list called `ingredients`.
   - Ask the user how many ingredients they’d like to enter.
   - Based on this number, run a `for` loop that collects each ingredient and then adds it to your temporary list, `ingredients`.

4. Convert the list `ingredients` into a string using the `join()` method, where each ingredient is joined to the other with a comma followed by a space `(,)`.

5. Create a new object from the `Recipe` model called `recipe_entry` using the details above.

6. Generate the `difficulty` attribute for this recipe by calling its `calculate_difficulty()` method.

7. Add this to the database through the `session` object, and `commit()` this change.

### Function 2: view_all_recipes()

1. Retrieve all recipes from the database as a list.

2. If there aren’t any entries, inform the user that there aren’t any entries in your database, and exit the function to return to the main menu. (Tip: to exit the function, simply use the `return None` statement.)

3. Loop through this list of recipes, and call each of their `__str__` methods to display each recipe.

### Function 3: search_by_ingredients()

1. Check if the table has any entries. Use the `count()` method like below to get the number of entries in the given table: `session.query(<model name>).count()`. If there aren’t any entries, notify the user, and exit the function.

2. Retrieve only the values from the `ingredients` column of the table, and store this into a variable called `results`.

3. Initialize an empty list called `all_ingredients`.

4. Go through each entry in `results`, split up the ingredients into a temporary list, and add each ingredient from this list to `all_ingredients`. Check each ingredient isn’t already on the list before adding.

5. Display these ingredients to the user, where each ingredient has a number displayed next to it. Ask them by which ingredients they’d like to search for recipes.

6. The user is allowed to pick these ingredients by typing the numbers corresponding to the ingredients, separated by COMMAS.

7. Check that the user’s inputs match the options available. Otherwise, inform the user and exit the function.

8. Based on the user’s selection as numbers, make a list of ingredients to be searched for, called `search_ingredients`, which contains these ingredients as strings.

9. Initialize an empty list called `conditions`. This list will contain `like()` conditions for every ingredient to be searched for.

10. Run a loop that runs through `search_ingredients`, and performs the following steps:

    - Make a search string called `like_term`, which is essentially the ingredient, surrounded by a `“%”` on either side (e.g., `“%Milk%”`).
    - Append the search condition containing `like_term` to the `conditions` list (e.g., `<Model name>.<column to search in>.like(like_term)`).

11. Retrieve all recipes from the database using the `filter()` query, containing the list `conditions`. Display these recipes using the `__str__` method.

### Function 4: edit_recipe()

1. Check if any recipes exist on the database, and continue only if there are any. Otherwise, exit this function.

2. Retrieve the `id` and `name` for each recipe from the database, and store them into `results`.

3. From each item in `results`, display the recipes available to the user.

4. The user gets to pick a recipe by its `id`. If the chosen `id` doesn’t exist, exit the function.

5. Retrieve the entire recipe that corresponds to this `id` from the database into a variable called `recipe_to_edit`.

6. Display the recipe, including only `name`, `ingredients` and `cooking_time`. `difficulty` isn’t editable since it is a calculated value. Display a number next to each attribute so that the user gets to pick one.

7. Ask the user which attribute they’d like to edit by entering the corresponding number. Remember to check the user’s input here.

8. Based on the input, use `if-else` statements to edit the respective attribute inside the `recipe_to_edit` object. Recalculate the `difficulty` using the object’s `calculate_difficulty()` method.

9. Commit these changes to the database.

### Function 5: delete_recipe()

1. Check if any recipes exist on the database, and continue only if there are any. Otherwise, exit this function.

2. Retrieve the `id` and `name` of every recipe in the database. List these out to the user to choose from.

3. Ask the user which recipe they’d like to delete by entering the corresponding `id`. Verify inputs here.

4. Based on the selected `id`, retrieve the corresponding object that exists on the database.

5. Ask the user if they’re sure that they’d like to delete this entry. If it’s a ‘yes’, perform the delete operation and commit this change. Otherwise, exit the function.

## Part 4: Design The Main Menu

The main menu will be contained in a `while` loop, where the condition to exit the loop will be based on the user’s choice. The condition can be such that the loop only continues if the user’s choice at any point is not quit. This main menu is similar to that of the previous Exercise, with the difference being that the function call for each option doesn’t pass through arguments like conn and cursor.

### Directions:

1. Inside this loop, lay out print statements that display six options:

   - Create a new recipe
   - View all recipes
   - Search for recipes by ingredients
   - Edit a recipe
   - Delete a recipe
   - Additionally, tell the user to type `quit` to quit the application.

2. Using `if-elif` statements, launch the corresponding function based on the user’s input. Use an `else` statement at the end to handle any malformed input by informing the users of this error and having the loop simply continue to its next iteration to display the main menu again.

3. Once the user chooses to quit, close `session` and `engine` with their respective `close()` methods, and the script ends there.

## Part 5: Final Steps:

1. Create a few recipes through the application.

2. Run through each option on the menu, testing the app’s functionality by reading, updating, and deleting entries in the database and taking screenshots of the terminal during these operations.

3. Upload the code as well as screenshots to your GitHub repository here for review.

## step 6 - Document the work in a “README.md” file.

## step 8 - Complete learning journal
````
