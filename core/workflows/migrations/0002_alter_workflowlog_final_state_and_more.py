# Generated by Django 5.0.6 on 2024-07-06 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workflows', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workflowlog',
            name='final_state',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Published'), (4, 'Closed'), (5, 'Deleted')], help_text='The state of the resource after the action was performed.', verbose_name='Final State'),
        ),
        migrations.AlterField(
            model_name='workflowlog',
            name='initial_state',
            field=models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Published'), (4, 'Closed'), (5, 'Deleted')], help_text='The state of the resource before the action was performed.', verbose_name='Initial State'),
        ),
    ]
