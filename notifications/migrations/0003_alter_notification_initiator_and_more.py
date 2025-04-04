# Generated by Django 5.1.4 on 2025-01-30 21:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_sub_url_id_notification_url_id'),
        ('user_profile', '0002_userprofile_created_at_userprofile_email_domain_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='initiator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='user_profile.userprofile'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('comment', 'Comment'), ('upvote', 'Upvote')], max_length=10),
        ),
        migrations.AlterField(
            model_name='notification',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
