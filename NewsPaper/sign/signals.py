from allauth.account.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import Group

@receiver(user_logged_in)
def assign_group_to_user(sender, request, user, **kwargs):
    group = Group.objects.get(name='common')
    user.groups.add(group)