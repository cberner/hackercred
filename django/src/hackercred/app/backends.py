from django.contrib.auth.models import User

#Authenticate the user based on email instead of username
class EmailAuthBackend:
    def authenticate(self, email=None, password=None):
        try:
            user = User.objects.get(email=email.lower())
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None 

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None