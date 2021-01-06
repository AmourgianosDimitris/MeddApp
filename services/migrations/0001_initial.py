# Generated by Django 3.1.2 on 2020-11-14 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('introduction', models.TextField()),
                ('services', models.TextField()),
                ('diseases', models.TextField()),
                ('preference', models.TextField()),
            ],
        ),
    ]