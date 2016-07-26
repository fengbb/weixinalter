#-*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response,get_object_or_404,render
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
#from dockerweb import rundockercmd,registryjson
#from dockerweb.models import *
import urllib
import json
import time
import random
import re
import os
def index(request):
    userdict = {"fengbaobao":"2","zhangsiwei":"3","jiangxuan01":"4"}
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    corpid = 'wx5ebaf88b004111e1'
    corpsecret = 'zo9QKEURG5HWELkZUi1G4hSEucx8lRx2gvpemhikEWpFkeusXuJnyi8wuThcSFo4'
    username = request.GET.get('username')
    pid =  userdict[username]
    print(pid)
    context =  request.GET.get('context')
    main_content = {
            "touser" : username,
            "toparty" : pid,
            "msgtype" : "text",
            "agentid":"1",
            "text" :{
                "content" : context,
            },
            "safe":"0"
        }
    #尝试从etcd中取token值，取不到的话调用微信接口生成token值
    etcdtoken = urllib.urlopen('http://172.16.121.150:4001/v2/keys/weixin/token').read().decode('utf-8')
    jsonvalue = json.loads(etcdtoken)
    try:
        vlaueexist = jsonvalue["errorCode"]
    except:
        vlaueexist = None
    if vlaueexist:
        token1 = urllib.urlopen('%s?corpid=%s&corpsecret=%s' %(gettoken_url,corpid,corpsecret)).read()
        token2 = json.loads(token1)
        token = token2['access_token']
        #alterresult = os.popen('/usr/bin/python /usr/local/script/weixinalter.py %s' %contentstr).read()
        writeetcd = os.popen('curl -L http://172.16.121.150:4001/v2/keys/weixin/token -XPUT -d value=%s -d ttl=7200' %token).read().decode('utf-8')
    else:
        token = jsonvalue["node"]["value"]
    print(token)
    sendmsg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' %token
    print(sendmsg_url)
    json_data = json.dumps(main_content)
    sendresult = urllib.urlopen(sendmsg_url,json_data).read().decode('utf-8')
    json_result = json.dumps(sendresult)
    print(sendresult)
    print(type(sendresult))
    return HttpResponse(json_result)
#puthon3
def weixinalter(request):
    userdict = {"fengbaobao":"2","zhangsiwei":"3","jiangxuan01":"4"}
    gettoken_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
    corpid = 'wx5ebaf88b004111e1'
    corpsecret = 'zo9QKEURG5HWELkZUi1G4hSEucx8lRx2gvpemhikEWpFkeusXuJnyi8wuThcSFo4'
    username = request.GET.get('username')
    pid =  userdict[username]
    #print(pid)
    context =  request.GET.get('context')
    main_content = {
            "touser" : username,
            "toparty" : pid,
            "msgtype" : "text",
            "agentid":"1",
            "text" :{
                "content" : context,
            },
            "safe":"0"
        }
    #尝试从etcd中取token值，取不到的话调用微信接口生成token值
    #etcdtoken = urllib.request.urlopen('http://192.168.153.75:4001/v2/keys/weixin/token').read().decode()
    etcdtoken = os.popen('curl -L  http://192.168.153.75:4001/v2/keys/weixin/token').read()
    #print(type(etcdtoken))
    #print(etcdtoken)
    jsonvalue = json.loads(etcdtoken)
    try:
        vlaueexist = jsonvalue["errorCode"]
    except:
        vlaueexist = None
    if vlaueexist:
        token1 = urllib.request.urlopen('%s?corpid=%s&corpsecret=%s' %(gettoken_url,corpid,corpsecret)).read().decode()
        #print(type(token1))
        #print(token1)
        token2 = json.loads(token1)
        token = token2['access_token']
        #alterresult = os.popen('/usr/bin/python /usr/local/script/weixinalter.py %s' %contentstr).read()
        #writeetcd = os.popen('curl -L http://192.168.153.75:4001/v2/keys/weixin/token -XPUT -d value=%s -d ttl=7200' %token).read().decode('utf-8')
        writeetcd = os.popen('curl -L http://192.168.153.75:4001/v2/keys/weixin/token -XPUT -d value=%s -d ttl=7200' %token).read()
    else:
        token = jsonvalue["node"]["value"]
    #print(token)
    sendmsg_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s' %token
    #print(sendmsg_url)
    json_data = json.dumps(main_content).encode()
    #print(type(json_data))
    #sendresult = urllib.request.urlopen(sendmsg_url,json_data).read().decode('utf-8')
    sendresult = urllib.request.urlopen(sendmsg_url,json_data).read().decode()
    json_result = json.dumps(sendresult)
    #print(sendresult)
    #print(type(sendresult))
    return HttpResponse(json_result)
