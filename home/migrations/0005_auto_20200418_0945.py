# Generated by Django 3.0.5 on 2020-04-18 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_felling'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='click',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='dis_like',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='like',
            field=models.IntegerField(default=0),
        ),
    ]
