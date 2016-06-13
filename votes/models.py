import json

from channels import Group
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel

from places.models import Place


class VoteQuerySet(models.QuerySet):
    def by_username_for_place_today(self, username, place_id):
        now = timezone.now()
        return self.filter(username=username, place_id=place_id,
                           created__date__gte=now)

    def for_place_today(self, place_id):
        now = timezone.now()
        return self.filter(place_id=place_id, created__date__gte=now)


class Vote(TimeStampedModel):
    username = models.CharField(_('username'), max_length=64)

    place = models.ForeignKey(
        'places.Place',
        verbose_name=_('Place')
    )

    objects = VoteQuerySet.as_manager()

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} voted for {} at {}'.format(self.username, self.place,
                                              self.created)

    @classmethod
    def update(cls, place_id, username):
        votes = cls.objects.by_username_for_place_today(username, place_id)
        if votes.exists():
            votes.delete()
        else:
            cls.objects.create(username=username, place_id=place_id)
        cls.send_notification(place_id)

    @classmethod
    def send_notification(cls, place_id):
        total = cls.objects.for_place_today(place_id).count()
        try:
            place = Place.objects.get(pk=place_id)
        except Place.DoesNotExist:
            return

        notification = {
            'place_id': place_id,
            'total': total,
            'users': place.voters,
            'most_wanted': Place.most_wanted()
        }
        Group('votes').send({
            'text': json.dumps(notification),
        })
