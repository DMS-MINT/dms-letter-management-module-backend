# Generated by Django 5.0.6 on 2024-08-11 16:31

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('READY', 'Ready'), ('SENDING', 'Sending'), ('SENT', 'Sent'), ('FAILED', 'Failed')], db_index=True, default='READY', max_length=255)),
                ('subject', models.CharField(max_length=255)),
                ('html', models.TextField()),
                ('plain_text', models.TextField()),
                ('sent_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
