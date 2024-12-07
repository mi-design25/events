# Generated by Django 5.1.2 on 2024-12-07 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_client_alter_herosection_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=200)),
                ('date', models.DateField()),
                ('capacity', models.IntegerField()),
                ('program', models.TextField()),
                ('image', models.ImageField(upload_to='Evenements/')),
            ],
        ),
    ]
