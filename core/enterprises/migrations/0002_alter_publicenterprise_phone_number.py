# Generated by Django 5.0.6 on 2024-08-11 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enterprises', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicenterprise',
            name='phone_number',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Phone Number'),
        ),
    ]
