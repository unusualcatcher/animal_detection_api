# Generated by Django 5.1.3 on 2024-11-30 20:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the animal', max_length=10)),
                ('latitude', models.FloatField(help_text="Latitude of the animal's location")),
                ('longitude', models.FloatField(help_text="Longitude of the animal's location")),
            ],
        ),
    ]
