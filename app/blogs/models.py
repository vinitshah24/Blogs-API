from django.db import models
from django.conf import settings


def upload_image(instance, filename):
    return "blogs/{user}/{filename}".format(user=instance.user, filename=filename)


class BlogsQuerySet(models.QuerySet):
    pass


class BlogsManager(models.Manager):
    def get_queryset(self):
        return BlogsQuerySet(self.model, using=self._db)


class Blogs(models.Model):
    # User instance .save()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_image, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BlogsManager()

    def __str__(self):
        # Only show 50 words to represent the obj
        return str(self.content)[:50]

    class Meta:
        verbose_name = 'Blogs Post'
        verbose_name_plural = 'Blogs Posts'

    # Is Owner or Read Only Permission
    @property
    def owner(self):
        return self.user
