from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Author
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


class NewsList(LoginRequiredMixin, ListView):
    queryset = Post.objects.filter(post_choice='NEW').order_by('-post_date')
    template_name = 'news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context


class ArticlesList(LoginRequiredMixin, ListView):
    queryset = Post.objects.filter(post_choice='ART').order_by('-post_date')
    template_name = 'articles_list.html'
    context_object_name = 'articles_list'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class ArticlesDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'articles.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context

class NewsSearch(LoginRequiredMixin, ListView):
    queryset = Post.objects.filter(post_choice='NEW').order_by('-post_date')
    template_name = 'news_search.html'
    context_object_name = 'news_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class ArticlesSearch(LoginRequiredMixin, ListView):
    queryset = Post.objects.filter(post_choice='ART').order_by('-post_date')
    template_name = 'articles_search.html'
    context_object_name = 'articles_search'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewsCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.add_post')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.post_choice = 'NEW'
        self.object.post_author = Author.objects.get(author_name_id=self.request.user.id)
        return super().form_valid(form)

class ArticlesCreate(PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('news.add_post')


    def form_valid(self, form):
        post = form.save(commit=False)
        post.post_choice = 'ART'
        return super().form_valid(form)

class NewsUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news_edit.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.change_post')


class ArticlesUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles_edit.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('news.change_post')


class NewsDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('news.delete_post')


class ArticlesDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('articles_list')
    permission_required = ('news.delete_post')

class CategoryListView(NewsList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(post_category=self.category).order_by('-post_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribes.all()
        context['category'] = self.category
        return context

@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribes.add(user)

    message = 'Вы успешно подписавлись на рассылку новостей категории'
    return render(request, 'subscribe.html', {'category': category, 'message': message})