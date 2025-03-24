# sales/models.py
from django.db import models
from apps.users.models import User

class SalePlatform(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField()
    class Meta:
        db_table = 'sale_platform'
        verbose_name = 'Sale Platform'
        verbose_name_plural = 'Sale Platforms'
        ordering = ['id']

    def __str__(self):
        return self.name

class Sale(models.Model):
    class STATUS(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    id = models.AutoField(primary_key=True)
    receipt_folio = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS.choices, default=STATUS.PENDING)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)
    platform = models.ForeignKey(SalePlatform, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    client = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'sales_sale'
        verbose_name = 'Sale'
        verbose_name_plural = 'Sales'
        ordering = ['id']


    def __str__(self):
        return f"Sale {self.id}"

class SaleDetail(models.Model):
    id = models.AutoField(primary_key=True)
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    amount = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True,blank=True)

    class Meta:
        db_table = 'sale_detail'
        verbose_name = 'Sale Detail'
        verbose_name_plural = 'Sale Details'
        ordering = ['id']

    def __str__(self):
        return f"SaleDetail {self.id}"