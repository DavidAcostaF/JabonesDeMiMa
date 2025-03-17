# purchases/models.py
from django.db import models
from apps.suppliers.models import Supplier

class Purchase(models.Model):
    id = models.AutoField(primary_key=True)
    receipt_folio = models.CharField(max_length=100)
    date = models.DateTimeField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        db_table = 'purchases_purchase'
        verbose_name = 'Purchase'
        verbose_name_plural = 'Purchases'
        ordering = ['id']

    def __str__(self):
        return f"Purchase {self.id}"
class PurchaseDetail(models.Model):
    id = models.AutoField(primary_key=True)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    ingredient = models.ForeignKey('recipes.Ingredient', on_delete=models.CASCADE)
    amount = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'purchase_detail'
        verbose_name = 'Purchase Detail'
        verbose_name_plural = 'Purchase Details'
        ordering = ['id']

    def __str__(self):
        return f"PurchaseDetail {self.id}"