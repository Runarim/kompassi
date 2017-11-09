# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2017-11-09 16:15
from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Q


def populate_room_event(apps, schema_editor):
    Room = apps.get_model('programme', 'Room')
    Event = apps.get_model('core', 'Event')
    Programme = apps.get_model('programme', 'Programme')

    for event in Event.objects.all():
        # room has programmes in event
        q = Q(programme__category__event=event)

        # - OR -
        # room is added to the schedule of the event
        q |= Q(view__event=event)

        # - AND -
        # room is not a copy but one of the original pre-copy rooms
        q &= Q(event__isnull=True)

        for room in event.venue.room_set.filter(q).distinct():
            original_room_id = room.id

            room.id = None
            room.event = event
            room.save(force_insert=True)

            new_room_id = room.id

            Programme.objects.filter(room=original_room_id).update(room=new_room_id)

        for view in event.view_set.all():
            view.rooms.set([Room.objects.get(event=event, slug=r.slug) for r in view.rooms.all()], clear=True)

    Room.objects.filter(event__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20170827_1818'),
        ('programme', '0057_room_event'),
    ]

    operations = [
        migrations.RunPython(populate_room_event),
    ]
