# Generated by Django 4.0.5 on 2022-06-11 07:21

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0034_event_cancelled"),
    ]

    operations = [
        migrations.AddField(
            model_name="person",
            name="discord_handle",
            field=models.CharField(
                blank=True,
                help_text="Full discord handle with number, ie. handle#0000. Events may use this to give you roles based on your participation.",
                max_length=63,
                validators=[django.core.validators.RegexValidator(regex="^.{3,32}#[0-9]{4,6}$")],
                verbose_name="Discord handle",
            ),
        ),
    ]