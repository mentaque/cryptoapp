# Generated by Django 4.2.1 on 2023-05-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cryptodata', '0005_alter_cryptocurrency_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='cryptocurrency',
            name='if_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
