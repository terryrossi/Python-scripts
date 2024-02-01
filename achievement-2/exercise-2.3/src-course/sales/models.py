from django.db import models

# Create your models here.
class Sale(models.Model):
    book = models.ForeignKey('books.Book', on_delete=models.CASCADE)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    salesperson = models.ForeignKey('salespersons.SalesPerson', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.book)