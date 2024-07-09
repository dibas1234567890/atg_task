from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from login_system.forms import CustomLoginForm, CustomRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import authenticate, login

from login_system.models import CustomerUserProfile


# Create your views here.
def custom_register_view(request):
    form = CustomRegisterForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            print('is valid')
            # CustomerUserProfile.objects.create(**form.cleaned_data)
            context = {'success':'success', 'title':'success'}
            request.session["message"] = "Succesfully Registered"
            return HttpResponseRedirect(reverse('home:login'))
    
    context = {'title': 'User Register Form', 'form':form}
    return render(request, 'register.html', context)

def custom_login(request):
    form = CustomLoginForm()
    context = {'form':form}

    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password = password)
    if user is not None:
        login(request, user)
        custom_user_object = CustomerUserProfile.objects.get(pk = user.id)
        if custom_user_object.user_type == 'patient':
            return HttpResponseRedirect(reverse('home:patienddashboard'))
        else: 
            return HttpResponseRedirect(reverse('home:doctordashboard'))
    else: 
        return render(request, 'login.html',context )
    
def patient_dashboard(request):
    user = request.user.id
    print(user)
    display_object = CustomerUserProfile.objects.get(pk=user)
    context = {'user_data': display_object}
    print(display_object.city)
    return render(request, 'patient_dashboard.html', context )

def doctor_dashboard(request):
    user = request.user.id
    print(user)
    display_object = CustomerUserProfile.objects.get(pk=user)
    context = {'user_data': display_object}
    print(display_object.city)
    return render(request, 'doctor_dashboard.html', context )


@login_required
def index_view(request):
    user = request.user
    context = {'user':user}
    return render(request, 'index.html' )
