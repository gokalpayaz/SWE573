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
from ..models import Tags, Story, Location, StoryPhoto, Date
from django.contrib.gis.geos import Point
from django.core.files.uploadedfile import InMemoryUploadedFile
from datetime import datetime

date_format = '%Y-%m-%d'

def create_post(request):
    # If user is submitting, request method will be post, if user is launching the page it will be get
    if request.method == 'POST':
        title = request.POST['title']
        text = request.POST['text']
        tags = request.POST.get('tags').split(',')
        location_name = request.POST['location-name']
        point = request.POST['location-point']
        radius = request.POST['radius']
        images = request.FILES.getlist('imageUpload[]')
        date_option = request.POST['date_option']



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

        date = Date()
        if date_option == "exact_date":
            exact_date_str = request.POST['exact_date']
            start_date = datetime.strptime(exact_date_str, '%Y-%m-%d').date()
            end_date = start_date
            date.start_date = start_date
            date.end_date = end_date
            date.year = start_date.year
            date.season = get_season(start_date)
        elif date_option == "interval":
            start_date_str = request.POST['start_date']
            end_date_str = request.POST['end_date']
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            date.start_date = start_date
            date.end_date = end_date
            avg_date = start_date + (end_date - start_date) / 2
            date.year = avg_date.year
            date.season = get_season(avg_date)
        else:
            date.year = request.POST['year']
            date.season = request.POST['season']

        date.story = story
        date.save()





        for image in images:
            story_photo = StoryPhoto(story=story, photo=image)
            story_photo.save()

        for tag_name in tags:
            if tag_name != '':
                tag, created = Tags.objects.get_or_create(tag=tag_name, story=story)
                tag.save()

        return render(request, 'memories/landing.html')
    
    else:

        return render(request, 'memories/create_post.html')
    


def get_season(date):
    if date.month == 12 or date.month < 3:
        return 'W'
    elif 3 <= date.month < 6:
        return 'S'
    elif 6 <= date.month < 9:
        return 'U'
    else:
        return 'F'
