# Generated by Django 5.0.6 on 2024-10-03 10:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letters', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=50, verbose_name='Action')),
                ('role', models.CharField(max_length=50, verbose_name='Role')),
                ('initial_state', models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Published'), (4, 'Rejected'), (5, 'Closed'), (6, 'Trashed')], verbose_name='Initial State')),
                ('final_state', models.IntegerField(choices=[(1, 'Draft'), (2, 'Submitted'), (3, 'Published'), (4, 'Rejected'), (5, 'Closed'), (6, 'Trashed')], verbose_name='Final State')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')),
                ('success', models.BooleanField(verbose_name='Success')),
                ('actor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workflow_logs', to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('resource', models.ForeignKey(max_length=255, on_delete=django.db.models.deletion.CASCADE, to='letters.letter', verbose_name='Resource')),
            ],
            options={
                'verbose_name': 'Workflow Log',
                'verbose_name_plural': 'Workflow Logs',
                'ordering': ['-timestamp'],
            },
        ),
    ]
