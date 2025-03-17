# recipes/models.py
from django.db import models

class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    measure_unit = models.CharField(max_length=100)
    stock = models.IntegerField()

    def __str__(self):
        return self.name

class RecipeDetail(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"RecipeDetail {self.id}"