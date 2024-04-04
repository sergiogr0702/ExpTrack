from django.contrib import admin
from .models import Category, Book

class BookAdmin(admin.ModelAdmin):
    fields = ['title', 'subtitle', 'authors', 'publisher', 'publisher_date', 'category', 'distribution_expense']

# Register your models here.
admin.site.register(Category)
admin.site.register(Book, BookAdmin)