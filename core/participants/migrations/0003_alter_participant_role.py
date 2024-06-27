# Generated by Django 5.0.6 on 2024-06-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='role',
            field=models.IntegerField(choices=[(1, 'Author'), (2, 'Primary Recipient'), (3, 'Carbon Copy Recipient'), (4, 'Blind Carbon Copy Recipient'), (5, 'Collaborator'), (6, 'Administrator')], help_text='Select the role of this participant.', verbose_name='Roles'),
        ),
    ]