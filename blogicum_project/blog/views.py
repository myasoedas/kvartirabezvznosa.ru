# blogicum/blog/views.py
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import CreateView

from .constants import NUMBER_OF_POSTS
from .forms import CommentForm, UserRegistrationForm
from .mixins import (AuthorRequiredMixin, PaginatorMixin, 
                     PostQueryMixin, PostCommentCountMixin)
from .models import Category, Comment, Post

from django_ckeditor_5.widgets import CKEditor5Widget


class CommentDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.post.id})


class CommentUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.post.id})


class PostCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        post = get_object_or_404(
            Post, id=self.kwargs['post_id'], is_published=True)
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class UserLoginView(LoginView):
    def get_redirect_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class UserProfileEditView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    template_name = 'blog/user.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


class UserProfileView(PostQueryMixin, DetailView,
                      PostCommentCountMixin, PaginatorMixin):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        if self.request.user == user:
            user_posts = self.get_filtered_posts(author=user)
        else:
            user_posts = self.get_filtered_posts(
                author=user, published_only=True)
        context.update(self.get_paginated_context(user_posts))
        return context


class UserRegisterView(CreateView):
    template_name = 'registration/registration_form.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class IndexListView(PostQueryMixin, PostCommentCountMixin, PaginatorMixin, ListView):
    model = Post
    context_object_name = 'page_obj'
    template_name = 'blog/index.html'

    def get_queryset(self):
        return self.get_filtered_posts(published_only=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update(self.get_paginated_context(queryset))
        return context


class CategoryPostsListView(ListView, PostCommentCountMixin, PaginatorMixin):
    model = Post
    context_object_name = 'page_obj'
    template_name = 'blog/category.html'

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        self.category = get_object_or_404(
            Category, slug=category_slug, is_published=True)
        return self.category.posts.filter(
            is_published=True,
            pub_date__lte=timezone.now()
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update(self.get_paginated_context(queryset))
        context['category'] = self.category
        return context


class PostDetailView(DetailView, PaginatorMixin):
    model = Post
    template_name = 'blog/detail.html'

    def get_object(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        if (
            not post.is_published
            or not post.category.is_published
            or (post.pub_date > timezone.now())
        ) and post.author != self.request.user:
            raise Http404("Пост не опубликован или отложен.")
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        comments = post.comments.select_related(
            'author').order_by('created_at')
        context.update(self.get_paginated_context(comments))
        context['form'] = CommentForm()
        return context


def rss_feed(request):
    """Генерация RSS-канала для лендинга."""
    rss_content = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <rss version="2.0" xmlns:yandex="http://news.yandex.ru" xmlns:media="http://search.yahoo.com/mrss/">
        <channel>
            <title>Остеопат Бикетова — Турбо-страницы</title>
            <link>https://osteopatbiketova.ru/</link>
            <description>Остеопат Бикетова: услуги, квалификация, контакты</description>
            <language>ru</language>
            
            <!-- Услуги -->
            <item>
                <title>Лечение кривошеи</title>
                <link>https://osteopatbiketova.ru/#services</link>
                <description>Исправление кривошеи с восстановлением естественного положения шейных позвонков.</description>
                <pubDate>Wed, 04 Dec 2024 08:00:00 +0000</pubDate>
                <yandex:full-text>
                    <![CDATA[
                    <header>
                        <h1>Лечение кривошеи</h1>
                        <figure>
                            <img src="https://osteopatbiketova.ru/static/img/index/krivosheya.jpg" alt="Лечение кривошеи">
                        </figure>
                    </header>
                    <p>Чувствуете напряжение в шее или ограниченность движений? Остеопат поможет исправить кривошею, восстановив естественное положение шейных позвонков.</p>
                    ]]>
                </yandex:full-text>
            </item>
            
            <item>
                <title>Лечение ЛОР-заболеваний</title>
                <link>https://osteopatbiketova.ru/#services</link>
                <description>Устранение причин синуситов, отитов и других ЛОР-заболеваний остеопатическими методами.</description>
                <pubDate>Tue, 03 Dec 2024 08:00:00 +0000</pubDate>
                <yandex:full-text>
                    <![CDATA[
                    <header>
                        <h1>Лечение ЛОР-заболеваний</h1>
                        <figure>
                            <img src="https://osteopatbiketova.ru/static/img/index/lor.jpg" alt="Лечение ЛОР-заболеваний">
                        </figure>
                    </header>
                    <p>Страдаете от частых синуситов, отитов или проблем с дыханием? Остеопатический подход может помочь улучшить работу ЛОР-органов, устраняя причины недугов.</p>
                    ]]>
                </yandex:full-text>
            </item>
            
            <!-- О враче -->
            <item>
                <title>О враче</title>
                <link>https://osteopatbiketova.ru/#about</link>
                <description>Бикетова Александра Викторовна — врач-остеопат с более чем 10-летним опытом работы.</description>
                <pubDate>Mon, 02 Dec 2024 08:00:00 +0000</pubDate>
                <yandex:full-text>
                    <![CDATA[
                    <header>
                        <h1>О враче</h1>
                        <figure>
                            <img src="https://osteopatbiketova.ru/static/img/index/osteopat-biketova.jpeg" alt="Остеопат Бикетова Александра">
                        </figure>
                    </header>
                    <p>Врач-остеопат с более чем 10-летним опытом работы, специализирующийся на лечении боли в спине, суставах, а также ЛОР-заболеваний и аллергий.</p>
                    <p>Образование: Санкт-Петербургская государственная педиатрическая медицинская академия (2004–2010 гг.).</p>
                    ]]>
                </yandex:full-text>
            </item>

            <!-- Контакты -->
            <item>
                <title>Контакты</title>
                <link>https://osteopatbiketova.ru/#contact</link>
                <description>Контактная информация для записи к врачу-остеопату.</description>
                <pubDate>Mon, 02 Dec 2024 08:00:00 +0000</pubDate>
                <yandex:full-text>
                    <![CDATA[
                    <header>
                        <h1>Контакты</h1>
                        <p>Санкт-Петербург, ул. Смолячкова, 12, к.2</p>
                        <p>Телефон: +7 911 986 63 08</p>
                        <p>Email: biketova_osteopat@mail.ru</p>
                    ]]>
                </yandex:full-text>
            </item>
        </channel>
    </rss>
    """
    return HttpResponse(rss_content, content_type="application/rss+xml")