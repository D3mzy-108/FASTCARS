from django.shortcuts import redirect, render
from django.contrib import auth
from django.contrib.auth import authenticate

from .forms import ProfileForm
from .models import User
from django.contrib.auth.decorators import login_required

# Create your views here.


# register view
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
                return redirect('register')
            else:
                user = User.objects.create_user(
                    username=username, email=email, password=password1)
                auth.login(request, user)
                return redirect('home')
        else:
            return redirect('register')

    context = {}

    return render(request, 'user/register.html', context)


# login view
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(email=email).exists():
            username = User.objects.get(email=email).username
        else:
            username = None

        if username is not None:
            user = authenticate(username=username, password=password)

            if user is not None and user.is_staff:
                auth.login(request, user)
                return redirect('dashboard')
            elif user is not None and not user.is_staff:
                auth.login(request, user)
                return redirect('home')
            else:
                return redirect('login')

        else:
            return redirect('login')

    context = {}

    return render(request, 'user/login.html', context)


@login_required
def edit_profile(request):
    user = User.objects.get(id=request.user.id)
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=user)
        
        if profile_form.is_valid():
            profile_form.save()
            return redirect('edit_profile')
    else:
        profile_form = ProfileForm(instance=user)
    
    context = {
        'user': user,
        'profile_form': profile_form,
    }
    return render(request, 'user/edit_profile.html', context)


def logout(request):
    auth.logout(request)

    return redirect('home')
