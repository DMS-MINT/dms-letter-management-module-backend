# Generated by Django 5.0.6 on 2024-06-19 10:51

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.IntegerField(choices=[(2, 'Author'), (3, 'Primary Recipient'), (4, 'Carbon Copy Recipient'), (5, 'Blind Carbon Copy Recipient'), (6, 'Collaborator')], help_text='Select the role of this participant.', verbose_name='Role')),
                ('last_read_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('received_at', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
        ),
    ]
