from rest_framework.permissions import IsAuthenticated
from news.models import News
from .serializers import (
    NewsListSerializer,
#     ArticleDeleteUpdateSerializer
    )
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView
#from .permissions import IsOwnerOrReadOnly


class NewsListAPIView(ListAPIView):
    serializer_class = NewsListSerializer
    model = serializer_class.Meta.model
    
    
    def get_queryset(self):
        title = self.kwargs['title']
        queryset = News.objects.filter(title__contains=title)
        return queryset 