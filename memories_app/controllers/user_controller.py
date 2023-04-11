
from ..models import CustomUser
from django.core.mail import send_mail
import string
import secrets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

class UserController():
    def create_user(self, request):
        try:
            # Check if user is already present:
            if CustomUser.objects.filter(username=request.data['username']).exists():            
                return {'success': False, 'message': 'Username already taken.'}
            

            user = CustomUser.objects.create(
                id = CustomUser.objects.latest('id').id+1,
                username=request.data['username'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name'],
                email=request.data['email'],
                birth_date=request.data['birth_date'],
                photo=request.data['photo'],
                password=request.data['password'],
            )
            user.set_password(user.password)
            user.save()
            return {'success': True, 'message': 'User created successfully.'}

        except Exception as e:
            return {'success': False, 'message': str(e)}

    def get_all_users(self):
        try:
            users = CustomUser.objects.all()
            return list(users.values())
        except Exception as e:
            return {'success':False, 'message':str(e)}
        
    def login_user(self,request):
        username = request.data['username']
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return {'success': True, 'message': 'Log in successful.'}
        else:
            return {'success': False, 'message': "Wrong username, password combination."}
        
    def reset_password(self,request):
        email = request.data['email']
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return {'success': False, 'message': "User name doesn't exists."}
        else:

            alphabet = string.ascii_letters + string.digits
            raw_password = ''.join(secrets.choice(alphabet) for i in range(10))
            user.set_password(raw_password)
            user.save()

            send_mail(
                'Your new password',
                f'Your new password is: {raw_password}',
                'noreply@memories.com',
                [email],
                fail_silently=False
            )
            return {'success': True, 'message': 'Password reset email sent'}
        