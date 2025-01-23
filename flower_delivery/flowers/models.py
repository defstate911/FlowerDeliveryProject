from django.db import models
#from django.contrib.auth.models import User  # Используем встроенную модель пользователя

class Bouquet(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image = models.ImageField(upload_to='flowers/img/', blank=True, null=True)


    def __str__(self):
        return self.name  # Удобное отображение названия в админке



