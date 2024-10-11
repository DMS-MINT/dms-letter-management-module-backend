# Generated by Django 5.0.6 on 2024-10-10 19:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0009_alter_tenant_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantprofile',
            name='tenant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_profile', to='tenants.tenant'),
        ),
        migrations.AlterField(
            model_name='tenantsetting',
            name='tenant',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tenant_settings', to='tenants.tenant'),
        ),
    ]
