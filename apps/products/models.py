# products/models.py
from django.db import models

class ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        db_table = 'product_category'
        verbose_name = 'Product Category'
        verbose_name_plural = 'Product Categories'
        ordering = ['id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    measure_unit = models.CharField(max_length=50)
    stock = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ingredient'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'
        ordering = ['id']

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    class Meta:
        db_table = 'product'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['id']

    def __str__(self):
        return self.name


class ProductIngredient(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'product_ingredient'
        verbose_name = 'Product Ingredient'
        verbose_name_plural = 'Product Ingredients'
        ordering = ['id']

    def __str__(self):
        return f"{self.ingredient.name} en {self.product.name}"
