from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from core.utils import NONUNIQUE_SLUG_FIELD_PARAMS, slugify


class Room(models.Model):
    event = models.ForeignKey('core.Event', null=True, blank=True, related_name='rooms')
    name = models.CharField(max_length=1023)
    order = models.IntegerField()
    notes = models.TextField(blank=True)
    slug = models.CharField(**NONUNIQUE_SLUG_FIELD_PARAMS)
    active = models.BooleanField(default=True)  # TODO kill with fire

    def __str__(self):
        return self.name

    def programme_continues_at(self, the_time, **conditions):
        criteria = dict(
            start_time__lt=the_time,
            length__isnull=False,
            **conditions
        )

        latest_programme = self.programme_set.filter(**criteria).order_by('-start_time')[:1]
        if latest_programme:
            return the_time < latest_programme[0].end_time
        else:
            return False

    class Meta:
        ordering = ['event', 'order']
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')
        unique_together = [
            ('event', 'slug'),
        ]

    @classmethod
    def get_or_create_dummy(cls):
        from core.models import Event
        event, unused = Event.get_or_create_dummy()
        return cls.objects.get_or_create(
            event=event,
            name='Dummy room',
            defaults=dict(
                order=0,
            )
        )


@receiver(pre_save, sender=Room)
def populate_room_slug(sender, instance, **kwargs):
    if instance.name and not instance.slug:
        instance.slug = slugify(instance.name)
