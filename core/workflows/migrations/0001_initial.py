# Generated by Django 5.0.6 on 2024-06-15 08:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letters', '0001_initial'),
        ('permissions', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkflowLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(help_text='The role of the user at the time of the action.', max_length=50, verbose_name='Role')),
                ('timestamp', models.DateTimeField(auto_now_add=True, help_text='The date and time when the action was performed.', verbose_name='Timestamp')),
                ('success', models.BooleanField(help_text='Indicates whether the action was successful.', verbose_name='Success')),
                ('action', models.ForeignKey(help_text='The action that was performed.', on_delete=django.db.models.deletion.CASCADE, to='permissions.permission', verbose_name='Action')),
                ('final_state', models.ForeignKey(help_text='The state of the resource after the action was performed.', on_delete=django.db.models.deletion.CASCADE, related_name='final_states', to='letters.state', verbose_name='Final State')),
                ('initial_state', models.ForeignKey(help_text='The state of the resource before the action was performed.', on_delete=django.db.models.deletion.CASCADE, related_name='initial_states', to='letters.state', verbose_name='Initial State')),
                ('resource', models.ForeignKey(help_text='The resource that was accessed or modified.', max_length=255, on_delete=django.db.models.deletion.CASCADE, to='letters.letter', verbose_name='Resource')),
                ('user', models.ForeignKey(help_text='The user who performed the action.', on_delete=django.db.models.deletion.CASCADE, related_name='access_logs', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Access Log',
                'verbose_name_plural': 'Access Logs',
                'ordering': ['-timestamp'],
            },
        ),
    ]
