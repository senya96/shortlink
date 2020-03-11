# Generated by Django 3.0.4 on 2020-03-08 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jwtoken',
            name='token',
        ),
        migrations.AddField(
            model_name='jwtoken',
            name='pub_key',
            field=models.TextField(default=''),
        ),
    ]
