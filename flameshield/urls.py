"""
URL configuration for flameshield project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.viewHomepage, name = "homepage"),
    path('contactUs/', views.contactUs, name = "contactUs"),
    path('home/', views.homeView, name = "home"),
    path('login/', views.loginView, name = "login"),
    path('report/', views.reportView, name = "report"),
    path('about/', views.aboutView, name = "about"),
    path('safety/', views.safetyView, name = "safety"),
    path('certificate/', views.certificateView, name = "certificate"),
    path('dashboard/', views.dashboardView, name= 'dashboardView'),
    path('map/<int:slug>', views.map, name= 'map'),
    path('addRestaurent/', views.addRestaurentView, name= 'addRestaurent'),
    path('displayContact/', views.displayContactView, name = "displayContact"),
    path('deleteContact/<int:slug>', views.deleteContact, name = "deleteContact"),
    path('signup/', views.signUpView, name = "signup"),
    path('clickPicture/', views.clickPicture, name = "clickPicture"),
    path('check/', views.check, name='check'),
    path('faceRecog/', views.faceRecog, name='faceRecog'),
    path('addTeam/', views.addTeam, name='addTeam'),
    path('deleteTeam/<int:slug>', views.deleteTeam, name = "deleteTeam"),
    path('deleteCertificate/<int:slug>', views.deleteCertificate, name = "deleteCertificate"),
    path('search/', views.searchReports, name='search_reports'),
    path('resolve/<int:slug>', views.resolve, name='resolve'),
    path('log/', views.log, name='log'),
    
   
    
]
