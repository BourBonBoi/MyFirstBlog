from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView

from .forms import AddPostForm
from .models import Posts, Category, Like
from .utils import DataMixin


class BlogHome(DataMixin, ListView):
    model = Posts
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # Добавьте категории здесь
        context['title'] = "Главная страница"
        context['popular_posts'] = Posts.objects.filter(is_published=True).order_by('-likes')[:5]
        return context

    def get_queryset(self):
        return Posts.objects.filter(is_published=True).select_related('category')


class ShowPost(DataMixin, DetailView):
    model = Posts
    template_name = 'blog/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=['post'])
        return dict(list(context.items()) + list(c_def.items()))


class PostsCategory(DataMixin, ListView):
    model = Posts
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allows_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['category_slug'])
        c_def = self.get_user_context(title='Категория - ' + str(c.name),
                                      cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Posts.objects.filter(category__slug=self.kwargs['category_slug'], is_published=True)


class AddPostView(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    success_url = ''  # Замените на URL, куда нужно редиректить после успешного добавления поста

    def form_valid(self, form):
        # Сохранение формы и присвоение пользователя
        post = form.save(commit=False)
        post.author = self.request.user  # Если у вас есть поле author в модели Posts
        post.save()
        return super().form_valid(form)


def like_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    # Проверяем, поставил ли уже пользователь лайк на данный пост
    if not Like.objects.filter(user=request.user, post=post).exists():
        # Если лайка нет, добавляем его
        Like.objects.create(user=request.user, post=post)
        post.likes += 1  # Увеличиваем счетчик лайков
        post.save()

    return redirect('post', post_slug=post.slug)  # Перенаправляем на страницу поста