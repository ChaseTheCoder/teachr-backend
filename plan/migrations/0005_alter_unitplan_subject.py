# Generated by Django 4.2.5 on 2023-09-22 23:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0004_rename_lessonplan_lessonoutline_lesson_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitplan',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='units', to='plan.plan'),
        ),
    ]
