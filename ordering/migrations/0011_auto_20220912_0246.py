# Generated by Django 3.2.13 on 2022-09-12 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0010_order_orderitems'),
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField()),
            ],
        ),
        migrations.AlterModelOptions(
            name='orderitems',
            options={'verbose_name_plural': 'categories'},
        ),
    ]
