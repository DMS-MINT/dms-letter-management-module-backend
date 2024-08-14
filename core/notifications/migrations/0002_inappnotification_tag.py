# Generated by Django 5.0.6 on 2024-08-14 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inappnotification',
            name='tag',
            field=models.IntegerField(choices=[(1, 'Mention'), (2, 'Inbox'), (3, 'Workflow'), (4, 'Ping'), (5, 'Reminder'), (6, 'Comment')], default=1),
        ),
    ]
