from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=50)
    color_hex = models.CharField(max_length=7)

    def __str__(self):
        return self.name

class Transaction(models.Model):

    class Type(models.TextChoices):
        EXPENSE = "EXPENSE", "expense"
        INCOME = "INCOME", "income"

    type = models.CharField(
        max_length=7,
        choices=Type.choices
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        sign = "-" if self.type == self.Type.EXPENSE else "+"
        return f"{sign}${self.amount:.2f}"

    @property
    def signed_amount(self):
        """Return amount with sign based on type."""
        if self.type == self.Type.EXPENSE:
            return -self.amount
        else:
            return self.amount
