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


