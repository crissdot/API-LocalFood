# Generated by Django 4.1.1 on 2023-01-16 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='category',
            table='categorias',
        ),
        migrations.AlterModelTable(
            name='product',
            table='platillos',
        ),
    ]
