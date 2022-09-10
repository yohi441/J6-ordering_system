from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_initial = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(max_length=2225, blank=True, null=True)
    cellphone_number = models.IntegerField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)


    def __str__(self):
        return self.user.username


class Barangay(models.Model):
    name = models.CharField(max_length=255)
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2)


class Food(models.Model):

    STATUS = [
        ('Best Seller', 'Best Seller'),
        ('Favorites', 'Favorites'),
        ('Special', 'Special'),
        ('Out Of Stock', 'Out Of Stock')
    ]

    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    status = models.CharField(
        max_length=50, choices=STATUS, default='Favorites')
    food_image = models.ImageField(
        upload_to='food_img/', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Testimonial(models.Model):
    full_name = models.CharField(max_length=100)
    message = models.TextField()
    avatar = models.ImageField(
        upload_to='testimonial/avatar/', null=True, blank=True)
    post_origin = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name

    @property
    def get_image(self):
        if not self.avatar:
            return '/static/assets/img/default.png'
        return self.avatar.url


class Catering(models.Model):
    package_set = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.package_set


class FoodList(models.Model):
    food_name = models.CharField(max_length=255)
    catering = models.ForeignKey(
        Catering, related_name="catering", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.food_name

