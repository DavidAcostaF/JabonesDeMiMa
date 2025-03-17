# expenses/models.py
from django.db import models
from apps.suppliers.models import Supplier

class ExpenseType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Expense(models.Model):
    id = models.AutoField(primary_key=True)
    receipt_folio = models.CharField(max_length=100)
    date = models.DateTimeField()
    description = models.TextField()
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.ForeignKey(ExpenseType, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def __str__(self):
        return f"Expense {self.id}"