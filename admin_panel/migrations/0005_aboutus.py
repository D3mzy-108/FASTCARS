# Generated by Django 3.2a1 on 2022-07-22 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_auto_20220721_1719'),
    ]

    operations = [
        migrations.CreateModel(
            name='AboutUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about_text', models.CharField(max_length=300)),
                ('sercive1', models.CharField(max_length=70)),
                ('sercive2', models.CharField(max_length=70)),
                ('sercive3', models.CharField(max_length=70)),
            ],
        ),
    ]
