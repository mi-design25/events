# Generated by Django 5.1.2 on 2024-12-11 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_message_read'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='organizer',
        ),
    ]
