# Generated by Django 5.0.6 on 2024-10-03 10:55

import core.enterprises.models
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name_en', models.CharField(max_length=255, unique=True, verbose_name='Name in English')),
                ('name_am', models.CharField(max_length=255, unique=True, verbose_name='Name in Amharic')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('phone_number', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Phone Number')),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Postal Code')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=core.enterprises.models.enterprise_directory_path, verbose_name='Logo')),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_address', to='common.address', verbose_name='Address')),
            ],
            options={
                'unique_together': {('name_en', 'name_am')},
            },
        ),
    ]
