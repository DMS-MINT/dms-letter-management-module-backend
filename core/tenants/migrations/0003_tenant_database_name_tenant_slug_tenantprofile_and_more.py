# Generated by Django 5.0.6 on 2024-10-09 17:46

import core.tenants.models.profile
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
        ('tenants', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenant',
            name='database_name',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='Database Name'),
        ),
        migrations.AddField(
            model_name='tenant',
            name='slug',
            field=models.SlugField(blank=True, verbose_name='Tenant URL Name'),
        ),
        migrations.CreateModel(
            name='TenantProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('contact_phone', models.PositiveBigIntegerField(blank=True, null=True, verbose_name='Contact Phone')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Contact Email')),
                ('postal_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Postal Code')),
                ('logo', models.ImageField(blank=True, null=True, upload_to=core.tenants.models.profile.tenant_directory_path, verbose_name='Logo')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tenant_address', to='common.address', verbose_name='Address')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_profile', to='tenants.tenant')),
            ],
            options={
                'verbose_name': 'Tenant Profile',
                'verbose_name_plural': 'Tenant Profiles',
            },
        ),
        migrations.CreateModel(
            name='TenantSetting',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auto_ref_number_letters', models.BooleanField(default=True, help_text='Enable to automatically generate reference numbers for letters. Disable for manual input.', verbose_name='Auto-generate Reference Numbers for Letters')),
                ('auto_date_letters', models.BooleanField(default=True, help_text='Enable to automatically generate reference numbers for letters. Disable for manual input.', verbose_name='Auto-generate Reference Numbers for Letters')),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_settings', to='tenants.tenant')),
            ],
            options={
                'verbose_name': 'Tenant Setting',
                'verbose_name_plural': 'Tenant Settings',
            },
        ),
    ]