from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Create your views here.
def register(request):
    #check request method to route
    if request.method == 'POST':
        #template form from django
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            #save to database
            form.save()
            #getdata from form
            username = form.cleaned_data.get('username')
            #f'' mean string formating in py 3.6
            messages.success(request, f'Your account {username} has been created! You are now able to login.')
            #redirecting
            return redirect('login')
    else:
        #template form from django
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form' : form})

@login_required
def profile(request):
    if request.method == 'POST':
        #populate form with current user information
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            #f'' mean string formating in py 3.6
            messages.success(request, f'Your account has been updated!')
            #redirecting
            return redirect('profile')
    else:
        #populate form with current user information
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form' : u_form,
        'p_form' : p_form
    }

    return render(request, 'users/profile.html', context)