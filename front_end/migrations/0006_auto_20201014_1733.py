# Generated by Django 3.0.7 on 2020-10-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('front_end', '0005_filmtalent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filmtalent',
            old_name='average_box_office_return',
            new_name='actor_average_box_office_return',
        ),
        migrations.RenameField(
            model_name='filmtalent',
            old_name='career_gross',
            new_name='actor_career_gross',
        ),
        migrations.RenameField(
            model_name='filmtalent',
            old_name='career_screen_average',
            new_name='actor_career_screen_average',
        ),
        migrations.RenameField(
            model_name='filmtalent',
            old_name='num_of_films',
            new_name='actor_num_of_films',
        ),
        migrations.RenameField(
            model_name='filmtalent',
            old_name='weeks_at_uk_cinemas',
            new_name='actor_weeks_at_uk_cinemas',
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='director_average_box_office_return',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='director_career_gross',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='director_career_screen_average',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='director_num_of_films',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='director_weeks_at_uk_cinemas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='writer_average_box_office_return',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='writer_career_gross',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='writer_career_screen_average',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='writer_num_of_films',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='filmtalent',
            name='writer_weeks_at_uk_cinemas',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]