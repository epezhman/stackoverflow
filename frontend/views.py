from django.db.models.query_utils import Q
from django.views.generic.base import TemplateView

from qa.models import Question


class Landing(TemplateView):
    template_name = 'frontend/landing.html'

    def get_context_data(self, **kwargs):
        search_term = self.request.GET.get('q')
        if search_term:
            questions = Question.objects.filter(Q(title__icontains=search_term) | Q(body__icontains=search_term))
        else:
            questions = Question.objects.all()
        return {
            'questions': questions
        }
