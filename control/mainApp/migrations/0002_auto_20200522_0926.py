# Generated by Django 2.2.1 on 2020-05-22 09:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='supplier',
            old_name='phone235',
            new_name='phone',
        ),
    ]
