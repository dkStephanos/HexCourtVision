# Generated by Django 3.2.9 on 2021-11-27 15:38

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ml_nba', '0002_candidatefeaturevector'),
    ]

    operations = [
        migrations.CreateModel(
            name='CandidateHexmap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hexmap', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=10), size=None)),
                ('cluster', models.IntegerField()),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.candidate')),
            ],
        ),
    ]
