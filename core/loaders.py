from django.conf import settings
from django.template.loaders.cached import Loader as CachedLoader


class ProductionCachedLoader(CachedLoader):
    """Template loader that caches templates only if the ``DEBUG`` settings is False."""

    def get_template(self, *args, **kwargs):
        if settings.DEBUG:
            self.reset()
        return super().get_template(*args, **kwargs)
