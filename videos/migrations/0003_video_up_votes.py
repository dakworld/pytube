# Generated by Django 2.0.6 on 2018-07-02 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20180701_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='up_votes',
            field=models.IntegerField(default=0),
        ),
    ]
