from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.utils import IntegrityError
from django.http.response import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext as _
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView

from rest_framework.viewsets import ModelViewSet

from . import models, forms
from .serializers import TagSerializer


class QuestionDetailView(FormView):
    form_class = forms.AnswerForm
    template_name = 'qa/question_detail.html'

    def get_question(self):
        return models.Question.objects.get(slug=self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question'] = self.get_question()
        return context

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.author = self.request.user
        instance.question = self.get_question()
        instance.save()
        return HttpResponseRedirect(instance.get_absolute_url())


class TagDetailView(DetailView):
    template_name = 'qa/tag_detail.html'
    model = models.Tag


class VoteView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        content_type = ContentType.objects.get(pk=self.kwargs.get('ct_pk'))
        instance = content_type.get_object_for_this_type(pk=self.kwargs.get('pk'))
        try:
            models.Vote.objects.create(
                type=self.kwargs.get('type'),
                content_object=instance,
                author=self.request.user
            )
        except IntegrityError:
            messages.add_message(self.request, messages.ERROR, _('You already voted!'))

        return instance.get_absolute_url()

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TagViewSet(ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = TagSerializer