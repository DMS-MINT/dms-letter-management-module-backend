# Generated by Django 5.0.6 on 2024-07-25 09:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('letters', '0002_initial'),
        ('participants', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='participant',
            name='letter',
            field=models.ForeignKey(help_text='Select the letter associated with this participant.', on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='letters.letter'),
        ),
        migrations.AddField(
            model_name='participant',
            name='user',
            field=models.ForeignKey(help_text='Select the user associated with this participant.', on_delete=django.db.models.deletion.CASCADE, related_name='participates_in', to='users.baseuser'),
        ),
        migrations.AlterUniqueTogether(
            name='participant',
            unique_together={('user', 'letter')},
        ),
    ]
