# Generated by Django 5.0.6 on 2024-10-11 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_alter_memberprofile_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberpreference',
            name='member',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='member_preferences', to='members.member'),
        ),
    ]
