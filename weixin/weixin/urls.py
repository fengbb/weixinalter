#-*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from alter import views
from alter.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'weixin.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^weixin/$', index), #主页
]

