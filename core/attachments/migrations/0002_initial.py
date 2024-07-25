# Generated by Django 5.0.6 on 2024-07-25 09:18

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
            model_name='attachment',
            name='letter',
            field=models.ForeignKey(help_text='The letter to which this attachment belongs.', on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='letters.letter', verbose_name='Letter'),
        ),
    ]
