from datetime import date
from django.shortcuts import render, redirect
from .models import *
from .forms import Registerform
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response

def registerview(request):
    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("login")
    form = Registerform()
    return render(request, template_name="register.html", context={"form":form})

def loginview(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['username'] = user.username
            messages.info(request, "Successfully Login")
            return redirect("home")
        else:
            messages.error(request, "Invalid Username and Password")
    return render(request, "login.html")

def postdata(request):
    if "username" in request.session.keys():
        username_obj = User.objects.get(username = request.session['username'])
        print("username", username_obj)
        if request.method == 'POST':
            model = Todolist()
            print("model", model)
            print("item", request.POST['item'])
            model.item = request.POST['item']
            model.is_completed = request.POST.get('is_completed',False)
            model.priority = request.POST['priority']
            model.user = username_obj
            model.save()
            subject = 'welcome to TODO list'
            message = f'Hi {username_obj}, thank you for adding list in TODO list.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [username_obj.email]
            send_mail( subject, message, email_from, recipient_list )
            return redirect("home")
        return render(request, 'post.html',{"username":username_obj})

def get(request):
    if "username" in request.session.keys():
        username_obj = User.objects.get(username = request.session['username'])
        if request.method == 'GET':
            model = Todolist.objects.filter(user=username_obj.id)
        return render(request, 'home.html', {'model': model})
    else:
        return redirect("login")

def updatedata(request, id):
    if "username" in request.session.keys():
        username_obj = User.objects.get(username = request.session['username'])
        model = Todolist.objects.get(id=id)
        if request.method =='POST':
            model.item = request.POST['item']
            model.is_completed = request.POST['is_completed']
            model.save()
            return redirect('home')
        return render(request, 'update.html',{'model' : model})

def deleteview(request, id):
    try:
        if "username" in request.session.keys():
            username_obj = User.objects.get(username = request.session['username'])
            model = Todolist.objects.get(id=id)
            model.delete()
            return redirect("home")
    except Exception as e:
        return ("Not Available")
    
def logoutview(request):
    del request.session['username']
    return redirect("login")


