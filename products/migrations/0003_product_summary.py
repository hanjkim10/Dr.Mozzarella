# Generated by Django 3.2.5 on 2021-07-09 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20210707_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='summary',
            field=models.TextField(default="NULL"),
            preserve_default=False,
        ),
    ]