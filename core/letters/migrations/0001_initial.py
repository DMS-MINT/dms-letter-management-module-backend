# Generated by Django 5.0.6 on 2024-06-17 03:46

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('reference_number', models.SlugField(unique=True, verbose_name='Reference Number')),
                ('subject', models.CharField(blank=True, help_text='Enter the subject of the letter.', max_length=255, null=True, verbose_name='Subject')),
                ('content', models.TextField(blank=True, help_text='Enter the content of the letter.', null=True, verbose_name='Content')),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Letter',
                'verbose_name_plural': 'Letters',
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
                ('delivery_person_name', models.CharField(blank=True, help_text='Name of the person responsible for delivery.', max_length=255, null=True, verbose_name='Delivery Person Name')),
                ('delivery_person_phone', models.CharField(blank=True, help_text='Phone number of the delivery person.', max_length=255, null=True, verbose_name='Delivery Person Phone')),
                ('shipment_id', models.CharField(blank=True, help_text='Unique identifier for the shipment.', max_length=255, null=True, verbose_name='Shipment ID')),
            ],
            options={
                'verbose_name': 'Outgoing Letter',
                'verbose_name_plural': 'Outgoing Letters',
            },
            bases=('letters.letter',),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255)),
                ('actions', models.ManyToManyField(to='permissions.permission')),
            ],
            options={
                'verbose_name': 'State',
                'verbose_name_plural': 'States',
            },
        ),
        migrations.AddField(
            model_name='letter',
            name='current_state',
            field=models.ForeignKey(help_text='Select the current state of the letter.', on_delete=django.db.models.deletion.CASCADE, to='letters.state'),
        ),
    ]
