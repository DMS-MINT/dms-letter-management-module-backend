# Generated by Django 5.0.6 on 2024-08-16 15:34

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseParticipant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('role', models.IntegerField(choices=[(1, 'Author'), (2, 'Primary Recipient'), (3, 'Carbon Copy Recipient'), (4, 'Blind Carbon Copy Recipient'), (5, 'Collaborator'), (6, 'Administrator')], verbose_name='Roles')),
                ('last_read_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('received_at', models.DateTimeField(blank=True, editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='EnterpriseParticipant',
            fields=[
                ('baseparticipant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.baseparticipant')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('participants.baseparticipant',),
        ),
        migrations.CreateModel(
            name='ExternalUserParticipant',
            fields=[
                ('baseparticipant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.baseparticipant')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('participants.baseparticipant',),
        ),
        migrations.CreateModel(
            name='InternalUserParticipant',
            fields=[
                ('baseparticipant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.baseparticipant')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('participants.baseparticipant',),
        ),
    ]
