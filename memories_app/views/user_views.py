from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from http.client import responses
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from ..controllers.user_controller import UserController
from ..models import CustomUser
from django.conf import settings

# redirect--> Django creates a redirect response that tells the client's web browser 
# to navigate to the specified URL. The client's web browser then sends a new HTTP request to the URL,
# and the server responds with a new HTTP response. 
# this means that if we have the corresponding view method, execution will switch to that method.
# render --> When you call the render function with a request object, the name of a template, 
# and a context dictionary, Django uses the specified template to generate an HTML response 
# that includes the content of the template with the context variables filled in. 
# The resulting HTML response is then returned to the client.

user_controller = UserController()


@csrf_exempt
@api_view(['POST'])
def create_user(request):
    response = user_controller.create_user(request)
    if response['success']:
        messages.success(request, response['message'])
        return redirect(reverse('users'))
    else:
        messages.error(request, response['message'])
        return redirect(reverse('signup'))

@login_required(login_url='login_user')
@api_view(['GET'])
def get_all_users(request):
    users = user_controller.get_all_users()
    context = {'users': users}
    return render(request, 'memories/users.html', context)


@csrf_exempt
@api_view(['POST'])
def login_user(request):
    response = user_controller.login_user(request)
    if response['success']:
        return redirect(reverse('users'))
    else:
        messages.error(request, response['message'])
        return render(request, 'memories/landing.html')
    
@login_required(login_url='login_user')
@api_view(['GET'])
def logout_user(request):
    if request.user != None:
        logout(request)
    return redirect("/")


@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    response = user_controller.reset_password(request)
    if response['success']:
        return redirect(reverse('users'))
    else:
        messages.error(request, response['message'])
        return render(request, 'memories/landing.html')
    
@login_required(login_url='login_user')
@api_view(['GET'])
def profile(request):

    user = request.user
    data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'username': user.username,
        'birth_date': user.birth_date,
        'photo': user.photo,
    }
    # return render(request, 'memories/profile.html', context)
    context = {
        'data': data,
    }
    return render(request, 'memories/profile.html', context)


@login_required(login_url='login_user')
@api_view(['POST'])
def update_profile(request):
    response = user_controller.update_profile(request)
    if response['success']:
        return redirect(reverse("profile"))
    else:
        messages.error(request, response['message'])
        return redirect(reverse('profile'))

