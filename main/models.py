from django.db import models

# Create your models here.


class Service(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.title


class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image_before = models.ImageField(upload_to='portfolio/')
    image_after = models.ImageField(upload_to='portfolio/')
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.title


