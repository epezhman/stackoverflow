from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _


class CreationModel(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Author'))
    created = models.DateTimeField(_('Creation Date'), auto_now_add=True)
    updated = models.DateTimeField(_('Update Date'), auto_now=True)

    class Meta:
        abstract = True


class QAModel(CreationModel):
    title = models.CharField(_('Title'), max_length=250)
    body = models.TextField(_('Body'))
    slug = models.SlugField(_('Slug'))

    votes = GenericRelation('Vote')

    def votes_total(self):
        return self.votes.upvotes().count() - self.votes.downvotes().count()

    class Meta:
        abstract = True


class Tag(CreationModel):
    name = models.CharField(_('Name'), max_length=50)
    slug = models.SlugField(_('Slug'))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('qa:tag_detail', args=[self.slug])

    class Meta:
        db_table = 'frontend_tag'
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Question(QAModel):
    tags = models.ManyToManyField(Tag, related_name='questions')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('qa:question_detail', args=[self.slug])

    class Meta:
        db_table = 'frontend_question'
        verbose_name = _('Question')
        verbose_name_plural = _('Questions')


class Answer(QAModel):
    question = models.ForeignKey(Question, related_name='answers')
    marked_as_answer = models.BooleanField(_('Marked as Answer'), default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.question.get_absolute_url() + '#answer-{}'.format(self.pk)

    class Meta:
        db_table = 'frontend_answer'
        ordering = ['-marked_as_answer', '-created']
        verbose_name = _('Answer')
        verbose_name_plural = _('Answers')


class VoteManager(models.Manager):
    def upvotes(self):
        return self.get_queryset().filter(type='up')

    def downvotes(self):
        return self.get_queryset().filter(type='down')


class Vote(CreationModel):
    TYPES = (
        ('up', _('Upvote')),
        ('down', _('Downvote')),
    )
    type = models.CharField(_('Type'), max_length=4, choices=TYPES)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    objects = VoteManager()

    def __str__(self):
        return self.type

    class Meta:
        db_table = 'frontend_vote'
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')
        unique_together = ['content_type', 'object_id', 'author']
