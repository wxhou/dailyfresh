# Generated by Django 2.2.24 on 2022-06-22 16:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goods',
            name='category',
            field=models.ForeignKey(help_text='商品类目', on_delete=django.db.models.deletion.CASCADE, related_name='category', to='goods.GoodsCategory'),
        ),
        migrations.AlterField(
            model_name='goodsimage',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='goods.Goods'),
        ),
    ]
