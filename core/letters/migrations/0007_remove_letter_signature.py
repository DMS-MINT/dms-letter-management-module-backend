# Generated by Django 5.0.6 on 2024-06-27 14:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0006_letter_signature'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='signature',
        ),
    ]
