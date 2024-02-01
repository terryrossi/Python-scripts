from django.db import models

# Create your models here.
class SalesPerson(models.Model):
    username = models.CharField(max_length=120)
    email = models.EmailField(max_length=120)
    phone = models.CharField(max_length=12)
    address = models.TextField()

    def __str__(self):
        return str(self.name)