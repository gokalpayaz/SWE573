
from ..models import User

class UserController():
    def create_user(self, request):
        try:
            user = User.objects.create(
                user_name=request.data.get('user_name'),
                name=request.data.get('name'),
                surname=request.data.get('surname'),
                email=request.data.get('email'),
                birthdate=request.data.get('birthdate'),
                photo=request.data.get('photo'),
                password=request.data.get('password'),
            )
            return {'success': True, 'message': 'User created successfully.'}
        except Exception as e:
            return {'success': False, 'message': str(e)}
        
    def get_all_users(self):
        try:
            users = User.objects.all()
            return list(users.values())
        except Exception as e:
            return {'success':False, 'message':str(e)}