# Generated by Django 2.2.4 on 2020-05-26 00:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0002_comment_message'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='comment',
            new_name='message',
        ),
    ]
