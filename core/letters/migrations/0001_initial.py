# Generated by Django 5.0.6 on 2024-08-03 18:40

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference_number', models.SlugField(unique=True, verbose_name='Reference Number')),
                ('current_state', models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Published'), (4, 'Rejected'), (5, 'Closed'), (6, 'Trashed')], verbose_name='States')),
                ('subject', models.CharField(blank=True, max_length=255, null=True, verbose_name='Subject')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Content')),
                ('submitted_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('published_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('trashed', models.BooleanField(default=False, verbose_name='Trashed')),
                ('hidden', models.BooleanField(default=False, verbose_name='Hidden')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
                'permissions': (('can_view_letter', 'Can view letter'), ('can_update_letter', 'Can update letter'), ('can_archive_letter', 'Can archive letter'), ('can_share_letter', 'Can share letter'), ('can_submit_letter', 'Can submit letter'), ('can_publish_letter', 'Can publish letter'), ('can_reject_letter', 'Can reopen letter'), ('can_retract_letter', 'Can retract letter'), ('can_close_letter', 'Can close letter'), ('can_reopen_letter', 'Can reopen letter'), ('can_comment_letter', 'Can comment letter'), ('can_trash_letter', 'Can trash letter'), ('can_restore_letter', 'Can restore letter'), ('can_permanently_delete_letter', 'Can permanently delete letter')),
            },
        ),
        migrations.CreateModel(
            name='Incoming',
            fields=[
                ('letter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='letters.letter')),
            ],
            options={
                'verbose_name': 'Incoming Letter',
                'verbose_name_plural': 'Incoming Letters',
            },
            bases=('letters.letter',),
        ),
        migrations.CreateModel(
            name='Internal',
            fields=[
                ('letter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='letters.letter')),
            ],
            options={
                'verbose_name': 'Internal Letter',
                'verbose_name_plural': 'Internal Letters',
            },
            bases=('letters.letter',),
        ),
        migrations.CreateModel(
            name='Outgoing',
            fields=[
                ('letter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='letters.letter')),
                ('delivery_person_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Delivery Person Name')),
                ('delivery_person_phone', models.CharField(blank=True, max_length=255, null=True, verbose_name='Delivery Person Phone')),
                ('shipment_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Shipment ID')),
            ],
            options={
                'verbose_name': 'Outgoing Letter',
                'verbose_name_plural': 'Outgoing Letters',
            },
            bases=('letters.letter',),
        ),
    ]
