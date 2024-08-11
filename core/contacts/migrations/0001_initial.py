# Generated by Django 5.0.6 on 2024-08-11 16:31

import core.contacts.models
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('full_name_en', models.CharField(max_length=500, verbose_name='Full Name In English')),
                ('full_name_am', models.CharField(max_length=500, verbose_name='Full Name In Amharic')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('address', models.CharField(max_length=255, verbose_name='Address')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to=core.contacts.models.profile_picture_directory_path, verbose_name='Profile Picture')),
            ],
        ),
    ]
