from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def sign_in(request):
    return render(request, 'sign_in.html')

def sign_up(request):
    errors = User.objects.validate_user(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account')
    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
    request.session['user_id'] = new_user.id
    request.session['first_name'] = new_user.first_name
    request.session['user_level'] = new_user.user_level
    return redirect('/')

def login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['user_level'] = user.user_level
        return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('/')

def admin(request):
    return render(request, 'admin.html')

def admin_login(request):
    errors = User.objects.validate_login(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/account/admin')
    else:
        user = User.objects.get(email=request.POST['email'])
        if user.user_level == 9:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['user_level'] = user.user_level
            return redirect('/admin/dashboard')
        else:
            return redirect('/')




