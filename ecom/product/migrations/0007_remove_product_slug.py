# Generated by Django 3.2 on 2021-06-28 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_alter_product_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
    ]
