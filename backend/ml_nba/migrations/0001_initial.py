# Generated by Django 3.1.2 on 2021-01-06 20:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('event_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('event_num', models.IntegerField()),
                ('event_msg_type', models.IntegerField()),
                ('event_action_type', models.IntegerField()),
                ('period', models.IntegerField()),
                ('period_time', models.CharField(max_length=5)),
                ('home_desc', models.CharField(max_length=100)),
                ('visitor_desc', models.CharField(max_length=100)),
                ('score', models.CharField(max_length=9)),
                ('directionality', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('color', models.CharField(max_length=7)),
                ('name', models.CharField(max_length=25)),
                ('abreviation', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('player_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('last_name', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=20)),
                ('jersey_number', models.IntegerField()),
                ('position', models.CharField(max_length=5)),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.team')),
            ],
        ),
        migrations.CreateModel(
            name='Moment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x_loc', models.FloatField()),
                ('y_loc', models.FloatField()),
                ('radius', models.FloatField(null=True)),
                ('index', models.IntegerField()),
                ('game_clock', models.FloatField()),
                ('shot_clock', models.FloatField()),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.event')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.player')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.team')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('game_date', models.CharField(max_length=20)),
                ('final_score', models.CharField(max_length=9)),
                ('home_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='home_team', to='ml_nba.team')),
                ('visitor_team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='visitor_team', to='ml_nba.team')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='ml_nba.game'),
        ),
        migrations.AddField(
            model_name='event',
            name='player_1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_1', to='ml_nba.player'),
        ),
        migrations.AddField(
            model_name='event',
            name='player_2',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_2', to='ml_nba.player'),
        ),
        migrations.AddField(
            model_name='event',
            name='player_3',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_3', to='ml_nba.player'),
        ),
        migrations.AddField(
            model_name='event',
            name='possesion_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.team'),
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('candidate_id', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('classification_type', models.CharField(max_length=20)),
                ('manual_label', models.BooleanField()),
                ('period', models.IntegerField()),
                ('game_clock', models.CharField(max_length=5)),
                ('shot_clock', models.FloatField()),
                ('player_a_name', models.CharField(max_length=25)),
                ('player_b_name', models.CharField(max_length=25)),
                ('notes', models.CharField(max_length=100)),
                ('event', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ml_nba.event')),
                ('player_a', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_a', to='ml_nba.player')),
                ('player_b', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='player_b', to='ml_nba.player')),
            ],
        ),
    ]
