# Generated by Django 4.2.1 on 2023-05-30 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptodata', '0002_alter_cryptocurrency_vwap_24h'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cryptocurrency',
            name='vwap_24h',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=100, null=True),
        ),
    ]