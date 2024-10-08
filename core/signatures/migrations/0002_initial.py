# Generated by Django 5.0.6 on 2024-10-08 19:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('signatures', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='lettersignature',
            name='signer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='signed_%(class)s', to=settings.AUTH_USER_MODEL, verbose_name='Signer'),
        ),
        migrations.AddField(
            model_name='userdefaultsignature',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='default_signature', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]
