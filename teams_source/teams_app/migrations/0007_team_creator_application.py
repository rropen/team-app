# Generated by Django 4.2.6 on 2024-02-23 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams_app', '0006_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='creator_application',
            field=models.CharField(default='unknown', max_length=128),
        ),
    ]
