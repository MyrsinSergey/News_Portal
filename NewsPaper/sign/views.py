from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from allauth.account.forms import LoginForm
from django.shortcuts import render

from news.models import Author


def login(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    return render(request, 'account/signup.html')

def logout_view(request):
    logout(request)
    return render(request, 'logout.html')

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/news'

@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')

    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

        Author.objects.create(author_name_id=request.user.pk)
    return redirect('/news')
