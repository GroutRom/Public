# Generated by Django 5.0.4 on 2024-05-07 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='uuid',
        ),
    ]
