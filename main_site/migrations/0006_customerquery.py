# Generated by Django 3.2a1 on 2022-07-26 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_site', '0005_customerreview'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomerQuery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=80)),
                ('message', models.TextField()),
            ],
        ),
    ]
