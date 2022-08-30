# Generated by Django 3.2.13 on 2022-08-29 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0002_remove_food_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkout',
            name='address',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AddField(
            model_name='checkout',
            name='cellphone',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='checkout',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='checkout',
            name='full_name',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='checkout',
            name='payment_method',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('Gcash', 'Gcash')], default='Gcash', max_length=200),
        ),
        migrations.AddField(
            model_name='checkout',
            name='total_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
