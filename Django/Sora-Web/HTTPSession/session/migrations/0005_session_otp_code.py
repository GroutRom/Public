# Generated by Django 5.0.6 on 2024-05-08 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0004_alter_user_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='otp_code',
            field=models.CharField(blank=True, max_length=6),
        ),
    ]
