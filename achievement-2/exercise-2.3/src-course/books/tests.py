from django.test import TestCase
from .models import Book

# Create your tests here.
class BookModelTest(TestCase):
     
    def setUpTestData():
        Book.objects.create(name='Big Data Analytics', author_name='John Doe', price='10.00', genre='classic',book_type='hardcover')
    
    def test_book_name(self):
       # Get a book object to test
       book = Book.objects.get(id=1)

       # Get the metadata for the 'name' field and use it to query its data
       field_label = book._meta.get_field('name').verbose_name

       # Compare the value to the expected result
       self.assertEqual(field_label, 'name')


    def test_author_name_max_length(self):
        # Get a book object to test
        book = Book.objects.get(id=1)
        # Get the metadata for the 'author_name' field and use it to query its max_length
        max_length = book._meta.get_field('author_name').max_length
        # Compare the value to the expected result i.e. 120
        self.assertEquals(max_length, 100)

    def test_book_name(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.name}'
        self.assertEquals(expected_object_name, 'Big Data Analytics')
    
    def test_author_content(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.author_name}'
        self.assertEquals(expected_object_name, 'John Doe')
    
    def test_price_content(self):
        book = Book.objects.get(id=1)
        expected_object_value = f'{book.price}'
        self.assertEquals(expected_object_value, '10.00')
    
    def test_stock_content(self):
        book = Book.objects.get(id=1)
        expected_object_name = f'{book.genre}'
        self.assertEquals(expected_object_name, 'classic')
