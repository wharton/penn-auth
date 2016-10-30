from django.contrib.auth.backends import RemoteUserBackend
from django.core.exceptions import PermissionDenied

from wharton_cosign_auth.utilities import call_wisp_api


class WhartonRemoteUserBackend(RemoteUserBackend):

    def authenticate(self, request, remote_user):
        # I think we need to implement this and only create the user if they
        # are in wharton AD.  I tried but was unable to get it to work when i
        # copied the method from
        # https://github.com/django/django/blob/master/django/contrib/auth/backends.py#L128
        pass

    def configure_user(self, user):
        response = call_wisp_api(
            'https://apps.wharton.upenn.edu/wisp/api/v1/adusers', {'username': user.username})
        if response['results']:
            results = response['results'][0]
            user.first_name = results['first_name']
            user.last_name = results['last_name']
            user.email = results['email'].replace('exchange.', '')

            '''
            Setting is_staff to True on the django user model
            Gives the user access to additional django functions
            '''
            user.is_staff = False
            user.save()

            return user
        else:
            '''
            Even though someone can login with Pennkey, there is a chance
            the user is not a Wharton user; in this case, raise a PermissionDenied
            '''
            raise PermissionDenied
