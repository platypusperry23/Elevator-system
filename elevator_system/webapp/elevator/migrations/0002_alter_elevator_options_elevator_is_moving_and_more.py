# Generated by Django 4.1.6 on 2023-02-05 21:46

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        ('elevator', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='elevator',
            options={'default_permissions': ('add', 'change', 'delete', 'read'), 'verbose_name': 'elevator', 'verbose_name_plural': 'elevators'},
        ),
        migrations.AddField(
            model_name='elevator',
            name='is_moving',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AddField(
            model_name='elevator',
            name='user_requests',
            field=models.CharField(max_length=10000, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
        migrations.AlterField(
            model_name='elevator',
            name='door_status',
            field=models.CharField(choices=[('OPEN', 'OPEN'), ('CLOSED', 'CLOSED')], default='CLOSED', max_length=10),
        ),
        migrations.AlterModelTable(
            name='elevator',
            table='elevator_details',
        ),
        migrations.CreateModel(
            name='UserRequests',
            fields=[
                ('request_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('modified_at', models.DateTimeField(auto_now=True, verbose_name='Modified at')),
                ('request_type', models.CharField(choices=[('open_door', 'open_door'), ('close_door', 'close_door'), ('choose_floor', 'choose_floor'), ('call_lift', 'call_lift'), ('stop', 'stop')], default=None, max_length=50, null=True)),
                ('from_floor', models.IntegerField(null=True)),
                ('to_floor', models.CharField(max_length=10000, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('elevator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='elevator.elevator')),
            ],
            options={
                'verbose_name': 'request',
                'verbose_name_plural': 'requests',
                'db_table': 'user_requests',
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'read'),
            },
        ),
    ]
