# Generated by Django 4.1.7 on 2023-04-18 06:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='wishlist',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cart.cart'),
        ),
    ]