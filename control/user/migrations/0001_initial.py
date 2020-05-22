# Generated by Django 2.2.1 on 2020-05-20 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentPostion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('department', models.CharField(max_length=20)),
                ('position', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=20)),
                ('department', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=6)),
                ('postionId', models.IntegerField()),
            ],
        ),
    ]