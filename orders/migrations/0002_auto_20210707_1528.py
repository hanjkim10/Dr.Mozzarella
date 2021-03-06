# Generated by Django 3.2.5 on 2021-07-07 15:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.orderstatus'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orders.itemstatus'),
        ),
    ]
