import random
import string
import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

# Create your models here.
class Category(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    creation_date = models.DateField(default=now)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique random number
            unique_id = self.generate_unique_id()
            while Category.objects.filter(id=unique_id).exists():
                unique_id = self.generate_unique_id()

            self.id = unique_id

        super().save(*args, **kwargs)

    def generate_unique_id(self):
        return int(''.join(random.choices(string.digits, k=13)))
    
    class Meta:
        db_table = 'categories'
    
class Book(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    subtitle = models.TextField(null=True, blank=True)
    authors = models.TextField(null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    publisher_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    distribution_expense = models.FloatField()
    creation_date = models.DateField(default=now)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique random number
            unique_id = self.generate_unique_id()
            while Book.objects.filter(id=unique_id).exists():
                unique_id = self.generate_unique_id()

            self.id = unique_id

        super().save(*args, **kwargs)

    def generate_unique_id(self):
        return int(''.join(random.choices(string.digits, k=13)))