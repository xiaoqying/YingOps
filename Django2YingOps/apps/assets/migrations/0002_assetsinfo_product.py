# Generated by Django 2.1.8 on 2020-04-14 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetsinfo',
            name='product',
            field=models.CharField(blank=True, default='', max_length=256, null=True, verbose_name='型号'),
        ),
    ]
