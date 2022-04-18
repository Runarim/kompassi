# Generated by Django 2.2.28 on 2022-04-18 12:53

from django.db import migrations
import localized_fields.fields.char_field
import psqlextra.manager.manager


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0029_auto_20220418_1531'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='ticketseventmeta',
            managers=[
                ('objects', psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        migrations.AddField(
            model_name='ticketseventmeta',
            name='terms_and_conditions_url',
            field=localized_fields.fields.char_field.LocalizedCharField(blank=True, default=dict, help_text='If set, customers will be required to indicate acceptance to finish order.', max_length=1023, required=[], verbose_name='Terms and conditions URL'),
        ),
    ]
