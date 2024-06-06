# Generated by Django 5.0.6 on 2024-06-06 16:11

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letters', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.IntegerField(choices=[(1, 'Blind Carbon Copy Recipient'), (2, 'Carbon Copy Recipient'), (3, 'Drafter'), (4, 'Forwarded Recipient'), (5, 'Forwarder'), (6, 'Recipient'), (7, 'Draft Reviewer'), (8, 'Sender'), (9, 'Workflow Manager')], help_text='Select the role of this participant.', verbose_name='Role')),
                ('is_reading', models.BooleanField(default=False, editable=False)),
                ('last_read_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('received_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('message', models.TextField(blank=True, help_text='Enter a message for the participant.', null=True, verbose_name='Message')),
                ('signature_image', models.ImageField(blank=True, help_text='Upload a signature image for the participant.', null=True, upload_to='signatures/', verbose_name='Signature Image')),
                ('letter', models.ForeignKey(help_text='Select the letter associated with this participant.', on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='letters.letter')),
            ],
            options={
                'verbose_name': 'Participant',
                'verbose_name_plural': 'Participants',
            },
        ),
    ]
