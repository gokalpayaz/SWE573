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
from ..controllers.user_controller import UserController


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

@csrf_exempt
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
    
@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    response = user_controller.reset_password(request)
    if response['success']:
        return redirect(reverse('users'))
    else:
        messages.error(request, response['message'])
        return render(request, 'memories/landing.html')
    
@login_required(login_url='login')
@api_view(['GET'])
def profile(request):
    user = user_controller.get_user_by_id(user_name=request.user.username)
    context = {'user': user}
    return render(request, 'memories/profile.html', context)