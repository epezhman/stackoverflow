from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'tag/(?P<slug>[\w-]+)$', views.TagDetailView.as_view(), name='tag_detail'),
    url(r'vote/(?P<type>(up|down)+)/(?P<ct_pk>[0-9]+)/(?P<pk>[0-9]+)$', views.VoteView.as_view(), name='vote'),
    url(r'(?P<slug>[\w-]+)$', views.QuestionDetailView.as_view(), name='question_detail'),
]
