# Generated by Django 4.0.5 on 2024-05-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log', models.CharField(max_length=500)),
            ],
        ),
    ]
