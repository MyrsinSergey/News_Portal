from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        group = Group.objects.get(name='common')
        user.groups.add(group)
        user.save()
        return user
