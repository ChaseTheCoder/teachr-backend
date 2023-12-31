# Generated by Django 4.2.5 on 2023-12-01 00:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0007_alter_unitplan_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unitplan',
            name='overview',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='unitplan',
            name='standard',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='unitplan',
            name='subject',
            field=models.ForeignKey(blank=True, default='', on_delete=django.db.models.deletion.CASCADE, related_name='units', to='plan.plan'),
        ),
        migrations.AlterField(
            model_name='unitplan',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
