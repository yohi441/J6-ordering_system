from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_initial = models.CharField(max_length=255)
    address = models.TextField(max_length=2225)
    cellphone_number = models.IntegerField()
    email_address = models.EmailField(blank=True, null=True)


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


class Checkout(models.Model):
    PAYMENT = [
        ('Cash on delivery', 'Cash on delivery'),
        ('Gcash', 'Gcash')
    ]

    food = models.ManyToManyField(Food)
    timestamp = models.DateTimeField(auto_now_add=True)
    sub_total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    address = models.CharField(max_length=1000, default="")
    cellphone = models.IntegerField(default=0)
    email = models.EmailField(blank=True, null=True)
    full_name = models.CharField(max_length=255, default="")
    payment_method = models.CharField(
        choices=PAYMENT, default='Gcash', max_length=200)
    barangay = models.ForeignKey(Barangay, related_name="barangay", on_delete=models.SET_NULL, blank=True, null=True)
    

    @property
    def total(self):
        return self.sub_total_price + self.barangay.shipping_fee


    def __str__(self):
        return self.full_name


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



class Order(models.Model):
    checkout = models.ForeignKey(Checkout, related_name="checkout", on_delete=models.SET_NULL, blank=True, null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=255)