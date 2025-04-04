# Generated by Django 5.1.4 on 2024-12-27 23:40

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('auth0_id', models.CharField(max_length=100, unique=True)),
                ('first_name', models.CharField(blank=True, default='', max_length=100)),
                ('last_name', models.CharField(blank=True, default='', max_length=100)),
                ('teacher_name', models.CharField(blank=True, default='', max_length=110)),
                ('title', models.CharField(blank=True, default='', max_length=50)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
            ],
        ),
    ]
