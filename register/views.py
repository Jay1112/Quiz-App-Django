from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import *

def register(request):
	form = RegisterForm()

	if request.user.is_authenticated:
		return redirect("/")

	if request.method == "POST":
		form = RegisterForm(request.POST)

		if form.is_valid():
			form.save()
			return redirect("/register/login")

	context = {
		"form":form,
	}

	return render(request,"register/register.html",context)

def login(request):

	if request.user.is_authenticated:
		return redirect("/")

	if  not request.user.is_authenticated and request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request,username=username,password=password)

		if user is not None:
			auth_login(request,user)
			return redirect("/")
		else:
			message = "Invalid Credentials"
			return render(request,"register/login.html",{"message":message})

	return render(request,"register/login.html",{})

def logout_request(request):
	logout(request)
	return redirect("/register/login/")

