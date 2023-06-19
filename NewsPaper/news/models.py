from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.core.cache import cache



class Author(models.Model):
    author_name = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    author_rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_posts_author = Post.objects.filter(post_author=self).aggregate(Sum('post_rating')).get('post_rating__sum') * 3
        rating_comments_author = Comment.objects.filter(user_name=self.author_name).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        rating_comments_posts = Comment.objects.filter(post__post_author=self).aggregate(Sum('comment_rating')).get('comment_rating__sum')
        self.author_rating = rating_posts_author + rating_comments_author + rating_comments_posts
        print(self.author_rating)
        self.save()

    def __str__(self):
        return f'{self.author_name} Рейтинг: {self.author_rating}'

class Category(models.Model):
    topics = models.CharField(max_length=20, unique=True)
    subscribes = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return f'{self.topics}'

class Post(models.Model):
    article = 'ART'
    new = 'NEW'
    TYPES = [
        (article, 'Статья'),
        (new, 'Новость')
    ]
    post_author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_choice = models.CharField(max_length=3, choices=TYPES, default=article)
    post_date = models.DateTimeField(auto_now_add=True)
    post_category = models.ManyToManyField(Category, through='PostCategory')
    post_title = models.CharField(max_length=255)
    post_text = models.TextField()
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()


    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.post_text[0:124] + '...'

    def get_absolute_url(self):
        return f'/news/{self.id}'

    def __str__(self):
        return f'{self.post_title.title()}: {self.post_text[:20]}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'articles-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.post}   Категория: {self.category}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_name = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

    def __str__(self):
        return f'{self.post}   Коментарий: {self.comment_text}  Опубликован: {self.comment_date}'