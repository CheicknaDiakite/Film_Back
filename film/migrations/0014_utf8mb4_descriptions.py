from django.db import migrations


def convert_description_columns_to_utf8mb4(apps, schema_editor):
    if schema_editor.connection.vendor != 'mysql':
        return

    statements = [
        "ALTER TABLE film_film MODIFY description LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL",
        "ALTER TABLE film_episode MODIFY description LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL",
        "ALTER TABLE film_pub MODIFY description LONGTEXT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL",
    ]

    with schema_editor.connection.cursor() as cursor:
        cursor.execute("ALTER DATABASE CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        for statement in statements:
            cursor.execute(statement)


class Migration(migrations.Migration):

    dependencies = [
        ('film', '0013_categorie_type_categorie'),
    ]

    operations = [
        migrations.RunPython(convert_description_columns_to_utf8mb4, migrations.RunPython.noop),
    ]
