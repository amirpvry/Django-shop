# Generated by Django 4.2.15 on 2024-09-05 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_productcategorymodel_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='discounted_price',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=10),
        ),
    ]
