from news.models import News
from rest_framework.serializers import ModelSerializer

class NewsListSerializer(ModelSerializer):
    class Meta:
        model = News
        fields =['newsid', 'title', 'username_uploader', 'news_url', 'score', 'type', 'sentimental']
        