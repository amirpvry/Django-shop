# Generated by Django 4.2.15 on 2024-09-21 22:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_productmodel_size'),
        ('cart_2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitemmodel',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.productmodel'),
        ),
    ]
