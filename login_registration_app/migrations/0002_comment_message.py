# Generated by Django 2.2.4 on 2020-05-25 23:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('message_uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_messages', to='login_registration_app.Register')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comment_uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='uploaded_comments', to='login_registration_app.Register')),
                ('message_comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages_comments', to='login_registration_app.Message')),
            ],
        ),
    ]
