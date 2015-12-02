from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers

from frontend import urls as frontend_urls
from qa import urls as qa_urls, views as qa_views


# API Routing
router = routers.DefaultRouter()
router.register(r'tag', qa_views.TagViewSet)

urlpatterns = [
    url(r'^qa/', include(qa_urls, namespace='qa')),
    url(r'^admin/', admin.site.urls),
    url(r'', include(frontend_urls, namespace='frontend')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls, namespace='api')),
]
