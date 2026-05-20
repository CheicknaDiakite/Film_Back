from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

UserModel = get_user_model()

class EmailOrUsernameModelBackend(ModelBackend):
    """
    Custom authentication backend to allow users to log in using either their
    username or their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username might be an email or a username
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
            
        try:
            # Check if user exists by matching either username or email exactly
            user = UserModel.objects.get(
                Q(username__iexact=username) | Q(email__iexact=username)
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user
            UserModel().set_password(password)
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
