# Generated by Django 4.0 on 2024-05-09 09:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_conversation_initiator_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='conversation_id',
            new_name='conversation',
        ),
    ]
