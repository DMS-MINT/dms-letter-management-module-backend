# Generated by Django 5.0.6 on 2024-08-26 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attachments', '0004_rename_uploaded_file_letterattachment_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='letterattachment',
            name='description',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Description'),
        ),
    ]
