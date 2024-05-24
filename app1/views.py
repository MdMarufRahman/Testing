import base64
import datetime
import os
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect, HttpResponse
from app1.models import contactUs as contactUsModel, report, addRestaurentModel, report, picture, TestUser, team, history
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .decorators import unauthenticated_user, admin_only


# Create your views here.

def homeView(request) :
    return render(request, "home.html")



def viewHomepage(request) :
               
    return render(request, "index.html") 

#Admin Dashboard
def DashBoardView(request):
    
    reports = report.objects.filter()
    report_count= len(reports)
    all_users = User.objects.all()
    user_count = len(all_users)
    all_certificates = addRestaurentModel.objects.filter()
    certificates_count = len(all_certificates)
    restaurents = addRestaurentModel.objects.filter()
    notification = contactUsModel.objects.filter()
    notification_count = len(notification)
    availableTeam = team.objects.filter()
    
    args = {
        "reports": reports,
        "report_count":report_count,
        "user_count":user_count,
        "certificates_count":certificates_count,
        "restaurents":restaurents,
        "notification_count":notification_count,
        "availableTeam":availableTeam

    }
    return render(request, 'adminDashboard.html', args)
    

def aboutView(request) :
    return render(request, "about.html")



def safetyView(request) :
    return render(request, "safety.html")





    





    
    

        
       
