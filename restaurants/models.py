# restaurants/models.py
from django.db import models
from django.contrib.auth.models import User

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)  # You might want to add choices here as well
    location = models.CharField(max_length=255)
    rating = models.FloatField(blank=True, null=True)  # Optional field for ratings

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    CUISINE_CHOICES = [
        ('Italian', 'Italian'),
        ('Chinese', 'Chinese'),
        ('Indian', 'Indian'),
        # Add more cuisines as needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cuisine = models.CharField(max_length=255, choices=CUISINE_CHOICES)
    favorite_dish = models.CharField(max_length=255)
    dietary_restrictions = models.TextField(blank=True)
    favorite_restaurants = models.ManyToManyField(Restaurant, related_name='favorited_by', blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reviews')
    content = models.TextField()
    rating = models.PositiveIntegerField(default=1)  # Rating from 1 to 5
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user_profile.user.username} for {self.restaurant.name}'
