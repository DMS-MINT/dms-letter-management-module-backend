# Generated by Django 5.0.6 on 2024-10-11 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberprofile',
            name='phone_number',
            field=models.PositiveBigIntegerField(blank=True, null=True, unique=True, verbose_name='phone number'),
        ),
    ]
