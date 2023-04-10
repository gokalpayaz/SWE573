
from ..models import User
from django.contrib import messages
from django.shortcuts import render, redirect

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
                if User.objects.filter(user_name=username).first().check_password(password):
                user = User.objects.get(user_name=username)

                if user.check_password(password):
                    user.set_last_login()
                    user.save()
                    return {'success': True, 'message': 'Log in successful.'}
                else:
                    return {'success': False, 'message': "Wrong username, password combination."}
        except Exception as e:
            return {'success':False, 'message': str(e)}


