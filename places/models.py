from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from django_extensions.db.models import TimeStampedModel
from stdimage import StdImageField
from stdimage.utils import UploadToUUID


class Place(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=255)

    image = StdImageField(
        _('Image'),
        upload_to=UploadToUUID(path='places'),
        variations=settings.IMAGE_THUMBNAIL_VARIATIONS,
        blank=True, null=True)

    address = models.CharField(_('Address'), max_length=255)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return self.name

    @property
    def today_rating(self):
        now = timezone.now()
        return self.vote_set.filter(created__date__gte=now).count()

    @property
    def voters(self):
        now = timezone.now()
        voters = self.vote_set.filter(created__date__gte=now).values_list(
            'username', flat=True)
        return sorted(list(voters)) or ['Nobody']

    def voted_by(self, username):
        now = timezone.now()
        return self.vote_set.filter(created__date__gte=now,
                                    username=username).exists()
