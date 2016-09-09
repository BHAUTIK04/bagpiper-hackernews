from django.shortcuts import render
from .models import News
import requests
from django.http.response import HttpResponse, Http404
# Create your views here.
import time

def home_view(request):
    return render(request, "home.html")

def error_view(request):
    return render(request, "error.html")

def news_view(request):
    print "i am here"
    try:
        if request.method == "GET":
            START = time.time()
            NEWS_LIST = News.objects.all()
            
            #top news list
            try:
                TOP_NEWS_RESPONSE = requests.get("https://community-hacker-news-v1.p.mashape.com/topstories.json?print=pretty",
                                headers={
                                    "X-Mashape-Key": "vJRxSBsTZimshceVBnrGdEtYfXNRp1H6jGmjsn9Fa3jLE32dKG",
                                    "Accept": "application/json"
                            })
                TOP_NEWS_ID = TOP_NEWS_RESPONSE.json()
            except Exception as e:
                print "Error in top story API"
                raise Http404
            #Old Published News ID- already exist in Database
            TOP_NEWS_ID_OLD = [i.newsid for i in NEWS_LIST]
             
            #New Published News ID 
            TOP_NEWS_ID_NEW = list(set(TOP_NEWS_ID) - set(TOP_NEWS_ID_OLD))
             
            #fetch news
            print len(TOP_NEWS_ID_NEW)
            for i in TOP_NEWS_ID_NEW:
                try:
                    RESPONSE = requests.get("https://community-hacker-news-v1.p.mashape.com/item/"+str(i)+".json?print=pretty",
                                  headers={
                                    "X-Mashape-Key": "vJRxSBsTZimshceVBnrGdEtYfXNRp1H6jGmjsn9Fa3jLE32dKG",
                                    "Accept": "application/json"
                                  })
                except Exception as e:
                    print "Error in get news api"
                    raise Http404
                #News DATA
                NEWS_DETAILS_RESPONSE = RESPONSE.json()
                NEWS_ID = NEWS_DETAILS_RESPONSE.get("id")
                NEWS_TYPE = NEWS_DETAILS_RESPONSE.get("type")
                TITLE = NEWS_DETAILS_RESPONSE.get("title")
                NEWS_SCORE = NEWS_DETAILS_RESPONSE.get("score")
                NEWS_BY = NEWS_DETAILS_RESPONSE.get("by")
                NEWS_URL = NEWS_DETAILS_RESPONSE.get("url")
                NEWS_TITLE = TITLE.encode('utf-8')
                 
                #Sentimental Analysis
                SENTI_DETAILS_RESP = requests.post("http://text-processing.com/api/sentiment/","text="+NEWS_TITLE)
                SENTI_RESP = SENTI_DETAILS_RESP.json()
                SENTI = SENTI_RESP.get("label")
                SENTI_PROB = SENTI_RESP.get("probability")
                SENTI_NEG = SENTI_PROB.get("neg")
                SENTI_POS = SENTI_PROB.get("pos")
                SENTI_NEUTRAL = SENTI_PROB.get("neutral")
                 
                #Create Record in News Table
                try:
                    N = News()
                    N.newsid = NEWS_ID
                    N.username_uploader = NEWS_BY
                    N.title = NEWS_TITLE
                    N.news_url = NEWS_URL
                    N.score = NEWS_SCORE
                    N.type = NEWS_TYPE
                    N.sentimental = SENTI
                    N.sent_positive = SENTI_POS
                    N.sent_negative = SENTI_NEG
                    N.sent_neutral = SENTI_NEUTRAL
                    print N
                    N.save()
                except Exception as e:
                    print "Error in saving data"
                    pass 
            END = time.time()
            try:
                NEWS_RETRIEVE = News.objects.filter(newsid__in=TOP_NEWS_ID)
            except Exception as e:
                print "Error in retrieval data."
                raise Http404
            
            print END - START
            return render(request, "news.html",{"news":NEWS_RETRIEVE})
        else:
            return HttpResponse("POST /news/ Not allowed")
    except Exception as e:
        print e
        return HttpResponse("Error!!")

def detail_view(request, newsid):
    try:
        NEWS = News.objects.filter(newsid=newsid)
        return render(request, "details.html", {"news":NEWS[0]})
    except Exception as e:
        return HttpResponse("Error....!!!!")    
    