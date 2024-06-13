# Generated by Django 5.0.6 on 2024-06-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0003_remove_participant_role_participant_permissions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='role_name',
            field=models.IntegerField(choices=[(1, 'Editor'), (2, 'Author'), (3, 'Primary Recipient'), (4, 'Carbon Copy Recipient'), (5, 'Blind Carbon Copy Recipient'), (6, 'Collaborator')], help_text='Select the role name of this participant.', verbose_name='Role Name'),
        ),
    ]