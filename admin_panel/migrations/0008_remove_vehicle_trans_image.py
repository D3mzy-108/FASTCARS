# Generated by Django 4.0.3 on 2022-07-29 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0007_auto_20220722_1240'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='trans_image',
        ),
    ]
