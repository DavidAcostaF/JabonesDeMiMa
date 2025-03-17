# sales/models.py
from django.db import models
from apps.users.models import User

class SalePlatform(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Sale(models.Model):
    id = models.AutoField(primary_key=True)
    receipt_folio = models.CharField(max_length=100)
    date = models.DateTimeField()
    status = models.CharField(max_length=100)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    platform = models.ForeignKey(SalePlatform, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Sale {self.id}"

class SaleDetail(models.Model):
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"SaleDetail {self.id}"