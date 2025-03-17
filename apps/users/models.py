from django.contrib.auth.models import AbstractUser
from django.db import models
# from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel



class User(AbstractUser):
    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["id"]

    def __str__(self):
        # Always return something logic to the model in __str__, and never use .format, use fstring instead
        return f"{self.first_name} {self.last_name}"
