# Generated by Django 2.2.6 on 2019-11-12 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poorapp', '0007_auto_20191112_1836'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentprocess',
            name='bank_account',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='paymentprocess',
            name='bkash_account',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='paymentprocess',
            name='transaction_num',
            field=models.SlugField(max_length=12, unique=True),
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='bank_account',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='birth_certificate_number',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='bkash_account',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='driving_license',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='nid_number',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='poorpeople',
            name='passport_number',
            field=models.IntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]