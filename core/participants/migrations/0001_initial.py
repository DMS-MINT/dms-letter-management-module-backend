# Generated by Django 5.0.6 on 2024-10-03 10:55

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contacts', '0002_initial'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('enterprises', '0001_initial'),
        ('letters', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_participants', to=settings.AUTH_USER_MODEL)),
                ('letter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='letters.letter')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='EnterpriseParticipant',
            fields=[
                ('baseparticipant_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='participants.baseparticipant')),
                ('enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enterprise_referenced_in_letters', to='enterprises.enterprise')),
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
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact_referenced_in_letters', to='contacts.contact')),
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
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participated_in_letters', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('participants.baseparticipant',),
        ),
        migrations.AddIndex(
            model_name='baseparticipant',
            index=models.Index(fields=['role', 'letter'], name='participant_role_b1271a_idx'),
        ),
    ]
