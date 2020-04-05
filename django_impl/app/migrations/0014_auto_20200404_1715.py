# Generated by Django 3.0.4 on 2020-04-04 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20200404_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractcard',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag'),
        ),
        migrations.AlterField(
            model_name='abstractdeck',
            name='tags',
            field=models.ManyToManyField(blank=True, to='app.Tag'),
        ),
        migrations.AlterField(
            model_name='cardlayout',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
