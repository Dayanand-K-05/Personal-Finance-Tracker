# core/models.py
from django.db import models
from django.contrib.auth.models import User # Django's built-in User model

# Model for categories (e.g., Food, Transport, Salary)
class Category(models.Model):
    # Each category belongs to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100) # Name of the category

    class Meta:
        # Ensure a user cannot have two categories with the exact same name
        unique_together = ('user', 'name')
        verbose_name_plural = "Categories" # Correct pluralization in admin

    def __str__(self):
        # String representation for the admin site
        return f"{self.name} ({self.user.username})"

# Model for individual financial transactions
class Transaction(models.Model):
    # Choices for transaction type (Income or Expense)
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    # Each transaction belongs to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    # Link to the Category model
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2) # Amount of the transaction
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES) # Income or Expense
    date = models.DateField() # Date of the transaction
    description = models.TextField(blank=True, null=True) # Optional description

    class Meta:
        # Order transactions by date in descending order by default
        ordering = ['-date']

    def __str__(self):
        # String representation for the admin site
        return f"{self.date} - {self.description or self.category.name} - {self.amount} ({self.transaction_type})"
