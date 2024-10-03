# Generated by Django 5.0.6 on 2024-10-03 10:55

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department_name_en', models.CharField(max_length=255, verbose_name='Department Name (English)')),
                ('department_name_am', models.CharField(max_length=255, verbose_name='Department Name (Amharic)')),
                ('abbreviation_en', models.CharField(max_length=3, verbose_name='Abbreviation (English)')),
                ('abbreviation_am', models.CharField(max_length=3, verbose_name='Abbreviation (Amharic)')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('contact_phone', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Contact Phone')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Contact Email')),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
                'unique_together': {('department_name_en', 'department_name_am', 'abbreviation_en', 'abbreviation_am')},
            },
        ),
        migrations.CreateModel(
            name='JobTitle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title_en', models.CharField(max_length=255, verbose_name='Job Title (English)')),
                ('title_am', models.CharField(max_length=255, verbose_name='Job Title (Amharic)')),
            ],
            options={
                'unique_together': {('title_en', 'title_am')},
            },
        ),
    ]
