# Generated by Django 3.2.13 on 2022-11-07 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0021_alter_cateringreserve_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.AlterField(
            model_name='cateringreserve',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
