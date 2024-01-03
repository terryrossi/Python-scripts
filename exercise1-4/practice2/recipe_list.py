import pickle

recipe = [{
  'Name':'Tea',
  'Ingredients':['Tea leaves', 'Water', 'Sugar'],
  'Cooking_time' : '5 minutes',
  'Difficulty': 'Easy'
},
{
  'Name':'Tea 2',
  'Ingredients':['Tea leaves 2', 'Water 2', 'Sugar 2'],
  'Cooking_time' : '5 minutes 2',
  'Difficulty': 'Easy 2'
}
]

with open('recipe_binary.bin', 'wb') as my_file:
  pickle.dump(recipe, my_file)

with open('recipe_binary.bin', 'rb') as my_file:
  recipes = pickle.load(my_file)
  recipe1 = recipes[0]
  recipe2 = recipes[1]

print('')
print('----- Recipe 1 -----')
print('')
print('Name : ' + recipe1['Name'])

print('Ingredients : ')
for ingredient in recipe1['Ingredients']: print("     " + ingredient)
print('Cooking time : ' + recipe1['Cooking_time'])
print('Difficulty ; ' + recipe1['Difficulty'])

print('')
print('')

print('----- Recipe 2 -----')
print('')
print('Name : ' + recipe2['Name'])

print('Ingredients : ')
for ingredient in recipe2['Ingredients']: print("     " + ingredient)
print('Cooking time : ' + recipe2['Cooking_time'])
print('Difficulty ; ' + recipe2['Difficulty'])
