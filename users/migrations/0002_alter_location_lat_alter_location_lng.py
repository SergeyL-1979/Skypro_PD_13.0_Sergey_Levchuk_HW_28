# Generated by Django 4.1.7 on 2023-03-19 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='lat',
            field=models.FloatField(null=True, verbose_name='lat'),
        ),
        migrations.AlterField(
            model_name='location',
            name='lng',
            field=models.FloatField(null=True, verbose_name='lng'),
        ),
    ]
