# Generated by Django 4.2.13 on 2024-06-11 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poorapp', '0040_alter_poorpeople_payment_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='doner',
            name='complete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='doner',
            name='request',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='doner',
            name='status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='food_time',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
