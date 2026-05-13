from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("film", "0005_alter_episode_id_alter_film_id_alter_type_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="film",
            name="view_count",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="episode",
            name="view_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
