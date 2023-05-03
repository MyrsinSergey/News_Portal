from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from django import forms
from django_filters.widgets import RangeWidget
from .models import Author, Category, Post, PostCategory, Comment


class PostFilter(FilterSet):

    title = CharFilter(
        field_name='post_title',
        label='Поиск по названию',
        lookup_expr='icontains',
    )

    author = ModelChoiceFilter(
        field_name='post_author__author_name',
        queryset=Author.objects.all(),
        label='Поиск по автору',
        empty_label='любой',
    )

    date = DateFilter(
        field_name='post_date',
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Начиная с даты',
        lookup_expr='date__gte')