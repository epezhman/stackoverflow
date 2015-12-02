from django import template
from django.contrib.contenttypes.models import ContentType
from .. import models


register = template.Library()


@register.assignment_tag
def get_top_tags():
    return models.Tag.objects.all()[:10]


@register.assignment_tag
def get_ct_pk(object):
    return ContentType.objects.get_for_model(object).pk