from django.db import models
from django.utils.text import slugify
from django.contrib.sites.models import Site


# Create your models here.


class AbstractNameSlugModel(models.Model):
    name = models.CharField('Name', max_length=200)
    slug = models.SlugField('Slug', max_length=200)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return u'https://' + Site.objects.get_current().domain + u'/%s:%s/' % \
            (slugify(self._meta.verbose_name), self.slug)
