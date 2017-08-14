# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
import subprocess
def index(request):
    args = ["fab","-f deploy_test.py deploy_tomcat"]
    a = subprocess.Popen(args,shell=True,cwd='/home/tuandk/fabric',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if a.wait() == 0:
        str_kq = a.communicate()[0]
        return HttpResponse(str_kq)
    else:
        return HttpResponse("ERROR")

def deploy(request):
    if (request.method =="POST"):
        path_file = request.POST['path_file']
        args = ["fab","-f","deploy_test.py","deploy_tomcat",":/opt/tomcat,"]
        args.append(path_file)
        a = subprocess.Popen(args,cwd='/home/tuandk/fabric',stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if a.wait() == 0:
            str_kq = a.communicate()[0]
            return HttpResponse(str_kq)
        else:
            str_kq = a.communicate()[1] + path_file
            return HttpResponse(str_kq)
    else:
        return HttpResponseRedirect("http://192.168.1.102:8000/polls/prepare_deploy/")
def prepare_deploy(request):
    template = loader.get_template('polls/prepare_deploy.html')
    return render(request,'polls/prepare_deploy.html')

def check_confirm(request):
    if (request.method =="POST"):
        path_file = request.POST['path_file_download']
        print ("%s" %(path_file))
        context = {'path_file':path_file}
        return render(request,'polls/check_confirm.html',context)
    else:
        return HttpResponseRedirect("http://192.168.1.102:8000/polls/prepare_deploy/")
