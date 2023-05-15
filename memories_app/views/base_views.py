from django.shortcuts import render, redirect
from django.urls import reverse

def base_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('landing_page'))
    else:
        return redirect(reverse('login'))
