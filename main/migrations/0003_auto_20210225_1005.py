# Generated by Django 3.1.5 on 2021-02-25 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_search'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='search_field',
            new_name='search_iin',
        ),
        migrations.AddField(
            model_name='search',
            name='search_number',
            field=models.CharField(default=0, max_length=12),
            preserve_default=False,
        ),
    ]
