# Generated by Django 4.2.5 on 2023-12-04 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0010_alter_lessonoutline_description_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='resource',
            new_name='unit_plan',
        ),
    ]