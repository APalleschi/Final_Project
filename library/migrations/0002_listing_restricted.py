# Generated by Django 3.0.4 on 2020-05-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='restricted',
            field=models.BooleanField(default=False),
        ),
    ]
