# Generated by Django 5.0.6 on 2024-09-30 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='type',
            field=models.CharField(choices=[('OTP_VERIFICATION', 'OTP Verification'), ('REGISTRATION', 'Registration'), ('NOTIFICATION', 'Notification')], db_index=True, default='NOTIFICATION', max_length=255),
        ),
    ]
