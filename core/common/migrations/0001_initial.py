# Generated by Django 5.0.6 on 2024-08-16 15:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city_en', models.CharField(max_length=100, verbose_name='City (English)')),
                ('city_am', models.CharField(max_length=100, verbose_name='City (Amharic)')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
                'unique_together': {('city_en', 'city_am')},
            },
        ),
    ]
