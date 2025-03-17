# suppliers/models.py
from django.db import models

class Supplier(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name