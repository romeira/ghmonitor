from django.db import models

from common.models import IndexedTimeStampedModel


class Repository(IndexedTimeStampedModel):
    owner = models.ForeignKey('users.User', related_name='repositories',
                              on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.owner.username}/{self.name}'

    class Meta:
        verbose_name_plural = 'Repositories'
        unique_together = ('owner', 'name')


class Commit(IndexedTimeStampedModel):
    oid = models.CharField(max_length=40)
    short_oid = models.CharField(max_length=15)
    message_head = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField()
    url = models.URLField()
    committer = models.CharField(max_length=255)

    repository = models.ForeignKey(Repository, related_name='commits',
                                   on_delete=models.CASCADE)

    class Meta:
        ordering = ('-date', )
        unique_together = ('oid', 'repository')

    def __str__(self):
        return self.short_oid
