# Generated by Django 3.0.4 on 2020-03-08 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jwt_auth', '0004_auto_20200308_1916'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jwtoken',
            name='user',
        ),
        migrations.AddField(
            model_name='jwtoken',
            name='token',
            field=models.TextField(default=''),
        ),
    ]
