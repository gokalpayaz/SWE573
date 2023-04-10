from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.gis.db import models as geo_models



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/<filename>
    return 'images/userphoto_{0}/{1}'.format(instance.user_name, filename)

class User(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    user_name = models.CharField(unique=True, max_length=20)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    birthdate = models.DateField()
    photo = models.ImageField(upload_to=user_directory_path)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    def set_last_login(self):
        self.last_login = timezone.now()

class Story(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    tags = models.ManyToManyField('Tags')

class Tags(models.Model):
    tag = models.CharField(max_length=20, unique=True)

class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=200)

class Location(models.Model):
    name = models.CharField(max_length=255)
    point = geo_models.PointField(null=True, blank=True)
    radius = models.FloatField(null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)

class Date(models.Model):
    season_choices = [
        ('W', 'Winter'),
        ('S', 'Spring'),
        ('U', 'Summer'),
        ('F', 'Fall'),
    ]

    start_date = models.DateField(null=True, blank=True)
    end_date  = models.DateField(null=True, blank=True)
    season = models.CharField(max_length=1, choices=season_choices, null=True, blank=True)
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
