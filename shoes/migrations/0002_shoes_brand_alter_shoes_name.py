# Generated by Django 4.2.1 on 2023-05-10 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoes',
            name='brand',
            field=models.CharField(default='brand', max_length=120, verbose_name='Бренд'),
        ),
        migrations.AlterField(
            model_name='shoes',
            name='name',
            field=models.CharField(default='shoes', max_length=120, verbose_name='Модель'),
        ),
    ]
