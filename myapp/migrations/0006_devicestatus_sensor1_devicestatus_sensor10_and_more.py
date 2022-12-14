# Generated by Django 4.0.5 on 2022-07-23 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_alter_devicestatus_pin10status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicestatus',
            name='sensor1',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor10',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor2',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor3',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor4',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor5',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor6',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor7',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor8',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='sensor9',
            field=models.FloatField(blank=True, default=0.0, max_length=50),
        ),
    ]
