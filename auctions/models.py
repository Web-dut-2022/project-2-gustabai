from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, default=None)

class Listing(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.CharField(max_length=200, blank=True, null=True, default='https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/No_image_3x4.svg/1280px-No_image_3x4.svg.png')
    created_at = models.DateTimeField(auto_now_add=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ManyToManyField("Category", blank=True, default=None)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='winner', blank=True, null=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Coment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    class Meta:
       ordering = ['-created_at']
