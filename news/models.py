from __future__ import unicode_literals

from django.db import models

# Create your models here.

class News(models.Model):
    newsid = models.IntegerField(unique=True)
    username_uploader = models.CharField(max_length=100)
    title = models.SlugField(max_length=500)
    news_url = models.URLField(null=True)
    score = models.IntegerField()
    type = models.CharField(max_length=50)
    sentimental = models.CharField(max_length=10)
    sent_positive = models.FloatField()
    sent_negative = models.FloatField()
    sent_neutral = models.FloatField()
    
    def __unicode__(self):
        return self.title
    
    def __str__(self):
        return self.title