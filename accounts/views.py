from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def profile_view(request):
    return render(request, 'accounts/user_profile.html')

from django.contrib.auth.decorators import login_required

@login_required
def intro_view(request):
    return render(request, 'intro.html')




