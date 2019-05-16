# Generated by Django 2.2.1 on 2019-05-10 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restosearch', '0008_zomatocity'),
    ]

    operations = [
        migrations.CreateModel(
            name='ZomatoCountry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='zomatocity',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restosearch.ZomatoCountry'),
        ),
    ]