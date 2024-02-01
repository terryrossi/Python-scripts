from django.test import TestCase
from recipes.models import Recipe
from users.models import User
from ingredients.models import Ingredient

# Create your tests here.
class RecipeModelTestCase(TestCase):
   
    def setUp(self):
        # Create a User instance
        self.user = User.objects.create(
            username = 'testuser',
            firstname = 'test',
            lastname = 'user',
            email = 'testuser@gmail.com',
            password = 'testpassword'
        )
        # Create an Ingredient instance
        self.ingredient1 = Ingredient.objects.create(name = 'Flour')
        self.ingredient2 = Ingredient.objects.create(name = 'Sugar')

        # Create a Recipe instance
        self.recipe = Recipe.objects.create(
            name = 'Test Recipe',
            userid = self.user,
            description = 'Test Description',
            cooking_time = 30,
            difficulty = 'easy'
        )
        # Add ingredients to the recipe
        self.recipe.ingredients.add(self.ingredient1, self.ingredient2)
        self.recipe.save()

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.userid, self.user)
        self.assertGreater(self.recipe.cooking_time, 0)
        self.assertIn(self.recipe.difficulty, ['easy', 'medium', 'hard'])