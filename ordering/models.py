from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class About(models.Model):
    about = models.TextField()

    def __str__(self) -> str:
        return f"{self.about}"


class Barangay(models.Model):
    name = models.CharField(max_length=255)
    shipping_fee = models.IntegerField()

    def __str__(self):
        return f"{self.name}"


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    middle_initial = models.CharField(max_length=1, blank=True, null=True)
    address = models.TextField(max_length=2225, blank=True, null=True)
    barangay = models.ForeignKey(Barangay, related_name="barangay", on_delete=models.CASCADE, blank=True, null=True)
    cellphone_number = models.IntegerField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}"



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
        return f"{self.name}"



class Testimonial(models.Model):
    full_name = models.CharField(max_length=100)
    message = models.TextField()
    avatar = models.ImageField(
        upload_to='testimonial/avatar/', null=True, blank=True)
    post_origin = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.full_name}"

    @property
    def get_image(self):
        if not self.avatar:
            return '/static/assets/img/default.png'
        return self.avatar.url


class Catering(models.Model):
    package_set = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.package_set}"


class FoodList(models.Model):
    food_name = models.CharField(max_length=255)
    catering = models.ForeignKey(
        Catering, related_name="catering", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.food_name}"


class Order(models.Model):
  
    order_status = [
        ('Cancel', 'Cancel'),
        ('Ongoing', 'Ongoing'),
        ('Recieved', 'Recieved')
    ]
    user = models.ForeignKey(User, related_name="user_order", on_delete=models.CASCADE)
    shipping_fee = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    paid_status = models.CharField(max_length=10)
    order_status = models.CharField(max_length=20, choices=order_status, default="Ongoing")
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{str(self.user).title()} - {self.created_at.strftime('%B %d, %Y')}"

    class Meta:
        ordering = ['created_at']


class OrderItems(models.Model):
    order = models.ForeignKey(Order, related_name="order", on_delete=models.CASCADE)
    food = models.ForeignKey(Food, related_name="food", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return f"{self.food}"


class CateringReserve(models.Model):
    package_choice = [
        ('Package A', 'Package A'),
        ('Package B', 'Package B'),
        ('Package C', 'Package C'),
        ('Package D', 'Package D'),
        ('Package E', 'Package E'),
        ('Package F', 'Package F'),
        ('Customize', 'Customize')
    ]
    catering_status = [
        ('Approve', 'Approve'),
        ('Ongoing/Pending', 'Ongoing/Pending'),
        ('Disapprove', 'Disapprove'),
        ('Cancel', 'Cancel')
    ]
    user = models.ForeignKey(User, related_name='catering_user', on_delete=models.CASCADE)
    date = models.DateField(unique=True)
    party_package = models.CharField(max_length=10, choices=package_choice, default='Package A')
    reserve_status = models.CharField(max_length=20, choices=catering_status, default='Ongoing/Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


    def __str__(self):
        return f"{self.user} - {self.created_at.strftime('%B %d, %Y')}"
