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
from ..models import Tags, Story, Location
from django.contrib.gis.geos import Point


def create_post(request):
    # If user is submitting, request method will be post, if user is launching the page it will be get
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        tag_ids = request.POST.getlist('tags')
        location_name = request.POST['location-name']
        point = request.POST['location-point']
        radius = request.POST['radius']
        images = request.FILES.getlist('imageUpload[]')
        print(location_name)
        print(point)

        story = Story(user=request.user, title=title, text=text)
        story.save()

        location = Location()
        location.name = location_name
        location.point = Point(float(point.split(",")[0]),float(point.split(",")[1]))
        location.radius = float(radius)
        location.story = story
        location.save()

        for tag_id in tag_ids:
            story.tags.add(tag_id)

        return render(request, 'memories/landing.html')
    
    else:
        tags = Tags.objects.all()
        context = {'tags': tags}
        return render(request, 'memories/create_post.html', context)
