# Generated by Django 4.2.13 on 2024-06-02 07:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poorapp', '0033_blooddoner_bdoner_pass'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doner',
            name='blood_groups',
        ),
        migrations.RemoveField(
            model_name='paymentprocess',
            name='bkash_account',
        ),
        migrations.RemoveField(
            model_name='poorpeople',
            name='blood_group',
        ),
        migrations.DeleteModel(
            name='BloodDoner',
        ),
    ]