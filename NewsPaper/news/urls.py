from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('news/', cache_page(60)(NewsList.as_view()), name='news_list'),
   path('news/<int:pk>/', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'),
   path('news/search/', NewsSearch.as_view(), name='news_search'),
   path('news/create/', NewsCreate.as_view(), name='news_create'),
   path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('articles/', cache_page(60)(ArticlesList.as_view()), name='articles_list'),
   path('articles/<int:pk>/', ArticlesDetail.as_view(), name='articles_detail'),
   path('articles/search/', ArticlesSearch.as_view(), name='articles_search'),
   path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
   path('articles/<int:pk>/edit/', ArticlesUpdate.as_view(), name='articles_update'),
   path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
   path('categories/<int:pk>/', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]