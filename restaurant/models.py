from django.contrib.auth.models import User
from django.db import models

# Модель блюда
class Dish(models.Model):

    CATEGORY_CHOICES = [
        ("salats", "Салати"),
        ("drinks", "Напої"),
        ("desserts", "Десерти"),
        ("meat", "М'ясо"),
        ("fast food", "Фаст-Фуд"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    ingredients = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='all')
    image = models.ImageField(upload_to='dishes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Модель отзыва о блюде
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="comments")
    rating = models.PositiveSmallIntegerField()  # рейтинг от 1 до 5
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.dish}'

