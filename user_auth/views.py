
   
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from social_django.models import UserSocialAuth
from django.conf import settings
import tweepy
import json

from requests_oauthlib import OAuth1Session
import sys, codecs

sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

from user_auth.models import OAuthTokenTemp
from .forms import TweetForm

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'

consumer_key = settings.SOCIAL_AUTH_TWITTER_KEY
consumer_secret = settings.SOCIAL_AUTH_TWITTER_SECRET


def callback(request):
    access_token = user.extra_data['access_token']['oauth_token']
    access_secret = user.extra_data['access_token']['oauth_token_secret']
    request_token = request.GET["oauth_token"]; # リクエストトークンは以前と同じもの
    verifier = request.GET["oauth_verifier"];
    oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=request_token,
            verifier=verifier)
    
    access_token_url = "https://api.twitter.com/oauth/access_token"
    # アクセストークン取得
    response = oauth.fetch_request_token(access_token_url)

    # DBに追加or更新
    try:
        # レコードが存在するか確認
        user = User.objects.get(id=response["user_id"])
        if user.access_token != response["oauth_token"]:
            # アクセストークンが変わった場合更新
            user.access_token = response["oauth_token"]
            user.access_token_secret = response["oauth_token_secret"]
            user.save()
    except User.DoesNotExist:
        # 存在しなかったら追加
        user = User()
        user.id = response["user_id"]
        user.access_token = response["oauth_token"]
        user.access_token_secret = response["oauth_token_secret"]
        user.save()

    # セッションにトークンを保存
    request.session["access_token"] = response["oauth_token"]

    # リダイレクト
    return redirect("user_auth.views.top_page")


        
@login_required
def top_page(request):
    oauth_client = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret
    )

    user = UserSocialAuth.objects.get(user_id=request.user.id)
    user_oauth_token = user.extra_data['access_token']['oauth_token']
    user_oauth_token_secret = user.extra_data['access_token']['oauth_token_secret']
    access_token_url = "https://api.twitter.com/oauth/access_token"
    # アクセストークン取得
    # response = oauth_client.fetch_request_token(access_token_url)

    try:
        # レコードが存在するか確認
        user = UserSocialAuth.objects.get(user_id=request.user.id)
        # user = OAuthTokenTemp.objects.get(id=request.user.id)
        if user.access_token != user_oauth_token:
            # アクセストークンが変わった場合更新
            oauth = OAuthTokenTemp(
                oauth_token = user_oauth_token,
                oauth_token_secret = user_oauth_token_secret
            )
            oauth.save()
    except request.user.is_authenticated:
        # 存在しなかったら追加
        oauth = OAuthTokenTemp(
                id = request.user.id,
                oauth_token = user_oauth_token,
                oauth_token_secret = user_oauth_token_secret
            )
        oauth.save()
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(user_oauth_token, user_oauth_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit = True)

    followerIDs = api.followers_ids("ユーザーID")

    followerDatas = []
    for followerID in followerIDs:
        followerData = {}
        data = api.get_user(followerID)
        followerData["Name"] = data.name
        followerData["Follow"] = data.friends_count
        followerData["Follower"] = data.followers_count
        followerData["Description"] = data.description
        followerData["TweetCount"] = data.statuses_count
        followerDatas.append(followerData)


    return render(request,'user_auth/top.html',{'user': user})


def tweet(request):
    form = TweetForm
    return redirect('user_auth/top.html')