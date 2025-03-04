from django.db import models
from django.contrib.auth.models import User

# Модель для услуг
class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title

# Модель для портфолио
class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_before = models.ImageField(upload_to='portfolio/')
    image_after = models.ImageField(upload_to='portfolio/')
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title

# Модель для расчетов
class Calculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    work_type = models.CharField(max_length=100)
    area = models.FloatField()
    material = models.CharField(max_length=100)
    include_materials = models.BooleanField(default=False)
    urgency = models.CharField(max_length=50)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2)
    labor_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.work_type} - {self.total_cost}"
