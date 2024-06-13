# Generated by Django 5.0.6 on 2024-06-13 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0002_initial'),
        ('permissions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='role',
        ),
        migrations.AddField(
            model_name='participant',
            name='permissions',
            field=models.ManyToManyField(to='permissions.permission'),
        ),
        migrations.AddField(
            model_name='participant',
            name='role_name',
            field=models.IntegerField(choices=[(1, 'Editor'), (2, 'Author'), (3, 'Primary Recipient'), (4, 'Carbon Copy Recipient'), (5, 'Blind Carbon Copy Recipient'), (6, 'Stakeholder')], default=1, help_text='Select the role name of this participant.', verbose_name='Role Name'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Role',
        ),
    ]