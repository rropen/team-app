# Generated by Django 4.2.2 on 2023-06-28 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams_app', '0002_role_relationship'),
    ]

    operations = [
        migrations.CreateModel(
            name='Satus',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=65, unique=True)),
            ],
        ),
    ]
