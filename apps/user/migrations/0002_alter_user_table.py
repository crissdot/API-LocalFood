# Generated by Django 4.1.1 on 2023-01-16 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='user',
            table='usuarios',
        ),
    ]