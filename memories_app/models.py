from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.gis.db import models as geo_models
from django.contrib.auth.models import AbstractUser



def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<username>/<filename>
    return 'images/userphoto_{0}/{1}'.format(instance.username, filename)

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to=user_directory_path)
    birth_date = models.DateField(null=True, blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='memories_app_users',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='memories_app_users',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
        
    def set_last_login(self):
        self.last_login = timezone.now()

class Story(models.Model):
    id = models.AutoField(primary_key=True, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    text = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    # tags = models.ManyToManyField('Tags')

class Tags(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)

class Like(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
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

class StoryPhoto(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to="images/story_photos")
