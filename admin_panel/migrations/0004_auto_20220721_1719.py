# Generated by Django 3.2a1 on 2022-07-21 16:19

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_auto_20220721_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='trans_image',
            field=models.ImageField(blank=True, null=True, upload_to='vehicle_images', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
        migrations.CreateModel(
            name='NewCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='new', to='admin_panel.vehicle')),
            ],
        ),
    ]
