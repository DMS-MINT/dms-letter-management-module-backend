# Generated by Django 5.0.6 on 2024-06-26 16:00

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letters', '0006_letter_signature'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(help_text='Upload the attachment file.', upload_to='letters/attachments/', verbose_name='File')),
                ('description', models.CharField(blank=True, help_text='A brief description of the attachment.', max_length=255, null=True, verbose_name='Description')),
                ('letter', models.ForeignKey(help_text='The letter to which this attachment belongs.', on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='letters.letter', verbose_name='Letter')),
            ],
            options={
                'verbose_name': 'Attachment',
                'verbose_name_plural': 'Attachments',
            },
        ),
    ]