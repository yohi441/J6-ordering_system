# Generated by Django 3.2.13 on 2022-09-04 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0003_auto_20220829_1306'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='checkout',
            name='food',
            field=models.ManyToManyField(to='ordering.Food'),
        ),
    ]
