# Generated by Django 5.0.6 on 2024-05-09 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0005_session_otp_code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='device',
            unique_together={('user', 'type', 'vendor_uuid')},
        ),
    ]
