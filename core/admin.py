# core/admin.py
from django.contrib import admin
from .models import Category, Transaction

# Register your models here so they appear in the Django admin interface.
admin.site.register(Category)
admin.site.register(Transaction)