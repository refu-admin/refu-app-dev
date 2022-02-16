from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
import tweepy
from django.conf import settings
from django.http import HttpResponse
import datetime
import tweepy
from django.http import JsonResponse
import json

def top(request):
    # return render(request, 'user_auth/top.html') 
    if request.user.is_authenticated:
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        consumer_key = settings.SOCIAL_AUTH_TWITTER_KEY
        consumer_secret = settings.SOCIAL_AUTH_TWITTER_SECRET
        access_token = user.extra_data['access_token']['oauth_token']
        access_secret = user.extra_data['access_token']['oauth_token_secret']
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        timeline = api.home_timeline()
        return render(request,'user_auth/top.html', {'user': user, 'timeline': timeline})
    else:
        return render(request,'user_auth/top.html')

@login_required
def top_page(request):
    user = UserSocialAuth.objects.get(user_id=request.user.id)

    return render(request,'user_auth/top.html',{'user': user})