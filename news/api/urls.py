from django.conf.urls import url

from .views import (
    NewsListAPIView
    )

urlpatterns = [
    url(r'^list/(?P<title>.+)$', NewsListAPIView.as_view(), name='list'),
#     url(r'^edit/(?P<id>[0-9]+)$', ArticleUpdateAPIView.as_view(), name='update'),
#     url(r'^delete/(?P<id>[0-9]+)$', ArticleDeleteAPIView.as_view(), name='delete'),
]
