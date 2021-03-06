# Generated by Django 3.2.5 on 2021-07-12 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_summary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='sales',
        ),
        migrations.RemoveField(
            model_name='product',
            name='stocks',
        ),
        migrations.AddField(
            model_name='option',
            name='sales',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='option',
            name='stocks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='score',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
    ]
