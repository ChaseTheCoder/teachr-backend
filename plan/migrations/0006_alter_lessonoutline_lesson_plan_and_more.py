# Generated by Django 4.2.5 on 2023-10-10 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0005_alter_unitplan_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonoutline',
            name='lesson_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lesson_outline', to='plan.lessonplan'),
        ),
        migrations.AlterField(
            model_name='lessonplan',
            name='unit_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lessons', to='plan.unitplan'),
        ),
        migrations.AlterField(
            model_name='material',
            name='lesson_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='materials', to='plan.lessonplan'),
        ),
        migrations.AlterField(
            model_name='resource',
            name='resource',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resources', to='plan.unitplan'),
        ),
    ]