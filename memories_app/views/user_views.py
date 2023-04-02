from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from http.client import responses
from rest_framework.decorators import api_view

from django.shortcuts import render
from ..controllers.user_controller import UserController

@csrf_exempt
@api_view(['POST'])
def create_user(request):
    user_controller = UserController()
    response = user_controller.create_user(request.body)
    return JsonResponse(response)

@csrf_exempt
@api_view(['GET'])
def get_all_users(request):
    user_controller = UserController()
    users = user_controller.get_all_users()
    context = {'users': users}
    return render(request, 'memories/users.html', context)
