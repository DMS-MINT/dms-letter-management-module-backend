# Generated by Django 5.0.6 on 2024-08-11 08:29

import core.enterprises.models
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PublicEnterprise',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name_en', models.CharField(help_text='Name in English', max_length=255, unique=True)),
                ('name_am', models.CharField(help_text='Name in Amharic', max_length=255, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('phone_number', models.PositiveBigIntegerField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('address', models.CharField(blank=True, default='Addis Ababa, Ethiopia', max_length=255, verbose_name='Address')),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Postal Code')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=core.enterprises.models.enterprise_directory_path, verbose_name='Logo')),
            ],
            options={
                'unique_together': {('name_en', 'name_am')},
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email Address')),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone Number')),
                ('address', models.CharField(blank=True, default='Addis Ababa, Ethiopia', max_length=255, verbose_name='Address')),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Postal Code')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='enterprises.publicenterprise')),
            ],
            options={
                'unique_together': {('enterprise', 'address')},
            },
        ),
    ]
