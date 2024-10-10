# Generated by Django 5.0.6 on 2024-10-09 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0003_tenant_database_name_tenant_slug_tenantprofile_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenant',
            name='database_name',
            field=models.CharField(default='default_database_name', max_length=255, unique=True, verbose_name='Database Name'),
            preserve_default=False,
        ),
    ]