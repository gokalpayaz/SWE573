
from ..models import User
from django.core.mail import send_mail
import string
import secrets
from django.contrib.auth import authenticate, login

class UserController():
    def create_user(self, request):
        try:
            # Check if user is already present:
            if User.objects.filter(user_name=request.data['username']).exists():            
                return {'success': False, 'message': 'Username already taken.'}
            

            user = User.objects.create(
                id = User.objects.latest('id').id+1,
                user_name=request.data['username'],
                name=request.data['name'],
                surname=request.data['surname'],
                email=request.data['email'],
                birthdate=request.data['birthdate'],
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
            users = User.objects.all()
            return list(users.values())
        except Exception as e:
            return {'success':False, 'message':str(e)}
        
    def login_user(self,request):
        try:
            username = request.data['username']
            if not User.objects.filter(user_name=username).exists():
                return {'success': False, 'message': "User name doesn't exists."}
            else:
                password = request.data['password']
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    user.set_last_login()
                    user.save()
                    return {'success': True, 'message': 'Log in successful.'}
                else:
                    return {'success': False, 'message': "Wrong username, password combination."}
        except Exception as e:
            return {'success':False, 'message': str(e)}

    def reset_password(self,request):
        email = request.data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
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
        
    def get_user_by_id(self,request):
        return User.objects.get(user_name = request.data['username'])