# Generated by Django 5.0.6 on 2024-10-05 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_alter_organizationprofile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organizationprofile',
            name='created',
        ),
        migrations.RemoveField(
            model_name='organizationprofile',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='organizationprofile',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='organizationprofile',
            name='schema_name',
        ),
        migrations.RemoveField(
            model_name='organizationprofile',
            name='slug',
        ),
    ]
