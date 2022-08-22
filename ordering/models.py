from distutils.command.upload import upload
from django.db import models



class Food(models.Model):

    STATUS = [
        ('Best Seller', 'Best Seller' ),
        ('Favorites', 'Favorites' ),
        ('Special', 'Special'),
        ('Out Of Stock','Out Of Stock')
    ]

    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS, default='Favorites')
    food_image = models.ImageField(upload_to ='food_img/', null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name



class Checkout(models.Model):
    food = models.ManyToManyField(Food, related_name="foods")
    timestamp = models.DateTimeField(auto_now_add=True)


class Testimonial(models.Model):
    full_name = models.CharField(max_length=100)
    message = models.TextField()
    avatar = models.ImageField(upload_to='testimonial/avatar/', null=True, blank=True)
    post_origin = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    @property
    def get_image(self):
        if not self.avatar:
            return '/static/assets/img/default.png'
        return self.avatar.url
