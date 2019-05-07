# Generated by Django 2.2 on 2019-05-07 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20190507_1105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponitem',
            name='status',
            field=models.CharField(choices=[('UNVERIFIED', 'unverified'), ('VALID', 'valid'), ('INVALID', 'invalid'), ('EXPIRED', 'expired')], default='UNVERIFIED', max_length=10),
        ),
    ]