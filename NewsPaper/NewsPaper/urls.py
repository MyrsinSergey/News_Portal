from django.contrib import admin
from django.urls import path, include
from allauth.socialaccount.views import SignupView

urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('', include('news.urls')),
   path('sign/', include('sign.urls')),
   path('accounts/', include('allauth.urls')),
   path('accounts/google/login/', SignupView.as_view(), name='socialaccount_login'),

]