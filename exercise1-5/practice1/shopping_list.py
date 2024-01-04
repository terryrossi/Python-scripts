class ShoppingList(object):
  def __init__(self,list_name):
    self.list_name = list_name
    self.shopping_list = []

  def add_item(self,item):
    if item not in self.shopping_list:
      self.shopping_list.append(item)

  def remove_item(self, item):
    try:
      self.shopping_list.remove(item)
    except:
      print("Item not found.")

  def view_list(self):
    print('')
    print(f"List of Items of : {self.list_name}")
    for item in self.shopping_list:
      print(item)
    
  def merge_lists(self, obj):
    # Creating a name for our new, merged shopping list
    merged_lists_name = 'Merged List - ' + str(self.list_name) + " + " + str(obj.list_name)

    # Creating an empty ShoppingList object
    merged_lists_obj = ShoppingList(merged_lists_name)

    # Adding the first shopping list's items to our new list
    merged_lists_obj.shopping_list = self.shopping_list.copy()

    # Adding the second shopping list's items to our new list -
    # we're doing this so that there won't be any repeated items
    # in the final list, if both source lists contain common
    # items between each other
    for item in obj.shopping_list:
            if not item in merged_lists_obj.shopping_list:
              merged_lists_obj.shopping_list.append(item)

    # Returning our new, merged object
    return merged_lists_obj

pet_store_list = ShoppingList("Pet Store Shopping List")

for item in ["dog food", "frisbee", "bowl", "collars","flea collars"]:
  pet_store_list.add_item(item)

pet_store_list.view_list()

pet_store_list.remove_item("flea collars")

pet_store_list.view_list()

pet_store_list.add_item("frisbee")

pet_store_list.view_list()

grocery_store_list = ShoppingList('Grocery Store shopping List')

for item in ["fruits", "vegetables", "rice", "ice cream"]:
  grocery_store_list.add_item(item)
grocery_store_list.view_list()

merged_list = pet_store_list.merge_lists(grocery_store_list)
merged_list.view_list()