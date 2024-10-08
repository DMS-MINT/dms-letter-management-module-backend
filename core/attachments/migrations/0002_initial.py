# Generated by Django 5.0.6 on 2024-08-16 15:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('attachments', '0001_initial'),
        ('letters', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='letterattachment',
            name='letter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='letter_attachments', to='letters.letter', verbose_name='Letter'),
        ),
    ]
