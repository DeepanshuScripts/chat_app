# Generated by Django 4.0 on 2024-05-08 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_otpuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OtpUser',
        ),
    ]
