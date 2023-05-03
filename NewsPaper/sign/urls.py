from django.urls import path
from .views import *



urlpatterns = [
    path('login/', login, name='login'),
    path('signup/', signup, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('upgrade/', upgrade_me, name='upgrade'),

]

