# Generated by Django 2.2 on 2019-05-07 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_crawltask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crawltask',
            name='status',
            field=models.CharField(choices=[('STARTED', 'started'), ('PENDING', 'pending'), ('RUNNING', 'running'), ('FINISHED', 'finished')], max_length=10),
        ),
    ]
