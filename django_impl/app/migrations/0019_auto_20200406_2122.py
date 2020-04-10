# Generated by Django 3.0.4 on 2020-04-06 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0018_auto_20200406_2120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abstractcard',
            name='answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='answer', to='app.AbstractCardFact'),
        ),
        migrations.AlterField(
            model_name='abstractcard',
            name='question',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='app.AbstractCardFact'),
        ),
    ]
