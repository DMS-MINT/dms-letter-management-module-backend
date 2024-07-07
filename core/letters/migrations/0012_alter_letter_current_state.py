# Generated by Django 5.0.6 on 2024-07-07 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('letters', '0011_letter_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='current_state',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Published'), (4, 'Rejected'), (5, 'Closed'), (6, 'Trashed')], help_text='Select the current state of the letter.', verbose_name='States'),
        ),
    ]
