# Generated by Django 5.0.2 on 2024-02-25 17:22

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("programme", "0124_programme_ropecon2024_blocked_time_slots_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="programme",
            name="ropecon2024_language_prog",
        ),
        migrations.AlterField(
            model_name="programme",
            name="ropecon2024_language",
            field=models.CharField(
                choices=[
                    ("finnish", "Finnish"),
                    ("english", "English"),
                    ("language_free", "Language-free"),
                    ("fin_or_eng", "Finnish or English"),
                    ("fin_and_eng", "Finnish and English"),
                    ("other", "Other"),
                ],
                default="finnish",
                help_text="Finnish - choose this, if only Finnish is spoken in your programme.<br><br>English - choose this, if only English is spoken in your programme.<br><br>Language-free - choose this, if no Finnish or English is necessary to participate in the programme (e.g. a workshop with picture instructions or a dance where one can follow what others are doing).<br><br>Finnish or English - choose this, if you are okay with either of the two languages. The programme team will contact you regarding the final choice of language.<br><br>Finnish and English - choose this, if your programme item will use both Finnish and English (e.g. if you will switch languages based on participants).<br><br>Other - choose this, if your programme is in a language other than Finnish or English. If chosen, please provide the title and description of your programme in the chosen language.",
                max_length=13,
                null=True,
                verbose_name="Choose the language used in your programme",
            ),
        ),
    ]