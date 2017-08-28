"""picktick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.main),
    url(r'^report_mainpost', views.mainpost),
    url(r'^signup/', views.signup, name = 'signup'),
    url(r'^report_signuppost', views.signuppost),
    url(r'^home/', views.home, name = "home"),
    url(r'^newreport/', views.createreport, name = 'create'),
    url(r'^report_postcreatereport/', views.postcreatereport, name='report'),
    url(r'^logout/', views.logout, name='log'),
    url(r'^checkreport/', views.checkreport, name='check'),
    url(r'^report_postcheck', views.postcheck, name='postcheck'),
    url(r'^lostpassword/', views.lostpassword, name='lostpassword'),
    url(r'^adminhome/', views.adminhome, name='adminhome'),
    url(r'^report_admincheck/', views.admincheck, name='admincheck'),
    url(r'^report_postadmincheck', views.postadmincheck, name='postadmincheck'),
    url(r'^report_admindetail/', views.admindetail, name='admindetail'),
]