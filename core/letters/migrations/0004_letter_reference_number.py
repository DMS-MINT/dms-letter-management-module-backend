# Generated by Django 5.0.6 on 2024-06-15 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0003_rename_permissions_state_actions'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='reference_number',
            field=models.SlugField(blank=True, null=True, verbose_name='Reference Number'),
        ),
    ]
