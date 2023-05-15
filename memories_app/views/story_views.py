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
from django.db.models import Q, Count
from django.contrib.gis.geos import fromstr
from django.contrib.gis.db.models.functions import Distance
date_format = '%Y-%m-%d'

@login_required(login_url='login')
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

        return redirect("/")
    
    else:

        return render(request, 'memories/create_post.html')
   
@login_required(login_url='login')
def search_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        title = request.POST['title']
        tags = request.POST.get('tags').split(',')
        location_name = request.POST['location-name']
        point = request.POST['location-point']
        radius = request.POST['radius']
        date_option = request.POST['date_option']

        # Get search inputs
        filters = []
        if username != '':
            filters.append(Q(user__username__icontains=username))
        if title != '':
            filters.append(Q(title__icontains=title))
        if tags:
            tags_query = Q()
            for tag in tags:
                tags_query |= Q(tags__tag__icontains=tag)
            filters.append(tags_query)
        if location_name:
            long = float(point.split(',')[0])
            lat = float(point.split(',')[1])
            selected_location = fromstr(f'POINT({long} {lat})', srid=4326)
            location_ids = Location.objects.annotate(distance=Distance('point', selected_location)).filter(Q(distance__lte=radius) | Q(name__icontains=location_name)).values_list('id', flat=True)
            location_query = Q(location__in=location_ids)  # using location instead of location_id
            filters.append(location_query)

        if date_option != '':
            if date_option == "exact_date":
                exact_date_str = request.POST['exact_date']
                exact_date = datetime.strptime(exact_date_str, '%Y-%m-%d').date()
                date_query = Q(date__start_date__lte=exact_date, date__end_date__gte=exact_date)
                filters.append(date_query)

            elif date_option == "interval":
                start_date_str = request.POST['start_date']
                end_date_str = request.POST['end_date']
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
                date_query = Q(date__start_date__lte=end_date, date__end_date__gte=start_date)
                filters.append(date_query)

            else:  # date_option == "season"
                year = request.POST.get('year', None)
                season = request.POST.get('season', None)
                year_query = Q(date__year=year) if year else Q()
                season_query = Q(date__season=season) if season else Q()
                date_query = year_query & season_query
                filters.append(date_query)


        if len(filters)==0:
            return render(request, 'memories/search_post.html')
        else:
            result = Story.objects.filter(*filters).distinct()
            return render(request, 'memories/search_post.html', {'story_list': result})


        
    else:
        return render(request, 'memories/search_post.html')

@login_required(login_url='login')
def landing_page(request):
    stories = Story.objects.annotate(like_count=Count('like')).order_by('-like_count')[:5]
    return render(request, 'memories/landing_page.html', {'story_list': stories})

@login_required(login_url='login')
def get_season(date):
    if date.month == 12 or date.month < 3:
        return 'W'
    elif 3 <= date.month < 6:
        return 'S'
    elif 6 <= date.month < 9:
        return 'U'
    else:
        return 'F'
