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

def robots_txt_view(request):
        lines = [
            "User-agent: *",
            "Disallow: /admin/",
            "Sitemap: https://osteopatbiketova.ru/sitemap.xml",
            "Sitemap: https://osteopatbiketova.ru/rss-feed.xml",
        ]
        return HttpResponse("\n".join(lines), content_type="text/plain")

def rss_feed(request):
        """Генерация RSS-канала для лендинга."""
        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
        <rss xmlns:yandex="http://news.yandex.ru"
            xmlns:media="http://search.yahoo.com/mrss/"
            xmlns:turbo="http://turbo.yandex.ru"
            version="2.0">
            <channel>
                <title>Остеопат Бикетова Санкт-Петербург</title>
                <link>https://osteopatbiketova.ru/</link>
                <description>Эффективное лечение боли в спине, суставах и ЛОР-заболеваний без медикаментов</description>
                <language>ru</language>

                <!-- Главная страница -->
                <item turbo="true">
                    <link>https://osteopatbiketova.ru/</link>
                    <turbo:content>
                        <![CDATA[
                        <header>
                            <h1>Остеопат в Санкт-Петербурге</h1>
                            <figure>
                                <img src="https://osteopatbiketova.ru/static/img/logo.jpg" alt="Логотип Остеопат Бикетова">
                            </figure>
                            <h2>Бикетова Александра Викторовна</h2>
                            <p>Эффективное лечение боли в спине, суставах и ЛОР-заболеваний без медикаментов</p>
                        </header>
                        <section>
                            <h2>Услуги врача остеопата</h2>
                            <ul>
                                <li>
                                    <figure>
                                        <img src="https://osteopatbiketova.ru/static/img/krivosheya.jpg" alt="Лечение кривошеи">
                                        <figcaption>Лечение кривошеи</figcaption>
                                    </figure>
                                    <p>Чувствуете напряжение в шее или ограниченность движений? Остеопат поможет восстановить естественное положение шейных позвонков.</p>
                                </li>
                                <li>
                                    <figure>
                                        <img src="https://osteopatbiketova.ru/static/img/lor.jpg" alt="Лечение ЛОР-заболеваний">
                                        <figcaption>Лечение ЛОР-заболеваний</figcaption>
                                    </figure>
                                    <p>Страдаете от частых синуситов, отитов или проблем с дыханием? Остеопатический подход поможет устранить причины.</p>
                                </li>
                                <li>
                                    <figure>
                                        <img src="https://osteopatbiketova.ru/static/img/allergiya.jpg" alt="Лечение аллергии">
                                        <figcaption>Лечение аллергии</figcaption>
                                    </figure>
                                    <p>Мучает аллергия? Остеопат поможет устранить причины реакций и восстановить баланс организма.</p>
                                </li>
                                <li>
                                    <figure>
                                        <img src="https://osteopatbiketova.ru/static/img/index/sustavi.jpg" alt="Лечение болезней суставов">
                                        <figcaption>Лечение болезней суставов</figcaption>
                                    </figure>
                                    <p>Боли в суставах мешают двигаться свободно? Остеопат поможет снять напряжение, улучшить подвижность и устранить причины дискомфорта.</p>
                                </li>
                                <li>
                                    <figure>
                                        <img src="https://osteopatbiketova.ru/static/img/index/zhkt.jpg" alt="Лечение заболеваний ЖКТ">
                                        <figcaption>Лечение заболеваний ЖКТ</figcaption>
                                    </figure>
                                    <p>Проблемы с пищеварением и постоянный дискомфорт? Остеопат поможет восстановить работу ЖКТ, устранив причины нарушений.</p>
                                </li>
                                <li>
                                    <figure>
                                        <img src="https://osteopatbiketova.ru/static/img/index/endokrinaya-sistema.jpg" alt="Лечение эндокринных патологий">
                                        <figcaption>Лечение эндокринных патологий</figcaption>
                                    </figure>
                                    <p>Страдаете от гормональных сбоев или проблем с эндокринной системой? Остеопат поможет восстановить баланс в организме и улучшить общее состояние.</p>
                                </li>
                            </ul>
                        </section>

                        <section>
                            <h2>О враче</h2>
                            <figure>
                                <img src="https://osteopatbiketova.ru/static/img/biketova.jpg" alt="Бикетова Александра Викторовна">
                                <figcaption>Бикетова Александра Викторовна</figcaption>
                            </figure>
                            <p>Врач-остеопат с 10-летним опытом работы. Специализация: лечение боли в спине, суставах, а также ЛОР-заболеваний и аллергий.</p>
                            <p><strong>Образование:</strong></p>
                            <ul>
                                <li>Санкт-Петербургская государственная педиатрическая медицинская академия (2004–2010 гг.)</li>
                                <li>Санкт-Петербургский государственный университет (2013–2017 гг.)</li>
                            </ul>
                            <p><strong>Повышение квалификации:</strong></p>
                            <ul>
                                <li>2013 г. – СПбГУ, «Общие принципы мануальной медицины, остеопатии»</li>
                                <li>2015 г. – СПбГУ, «Остеопатическая диагностика и коррекция конечностей»</li>
                                <li>2019 г. – Институт остеопатической медицины, «Остеопатические аспекты педиатрии»</li>
                            </ul>
                        </section>

                        <section>
                            <h2>Запишитесь на консультацию</h2>
                            <p><strong>Адрес:</strong> Санкт-Петербург, ул. Смолячкова, 12, к.2</p>
                            <p><strong>Телефон:</strong> <a href="tel:+79119866308">+7 911 986 63 08</a></p>
                            <p><strong>Email:</strong> <a href="mailto:biketova_osteopat@mail.ru">biketova_osteopat@mail.ru</a></p>
                            <p><strong>WhatsApp:</strong> <a href="https://wa.me/79119866308">Написать</a></p>
                            <iframe src="https://yandex.ru/map-widget/v1/?ll=30.345564%2C59.971724&mode=search&ol=geo&ouri=ymapsbm1%3A%2F%2Fgeo%3Fdata%3DCgoxNDk2NTI3ODA2ElPQoNC-0YHRgdC40Y8sINCh0LDQvdC60YIt0J_QtdGC0LXRgNCx0YPRgNCzLCDRg9C70LjRhtCwINCh0LzQvtC70Y_Rh9C60L7QstCwLCAxMtC6MiIKDRa_8kEV2-JvQg%2C%2C&z=17.78" 
                                width="560" height="400" frameborder="0" allowfullscreen="true" style="position:relative;">
                            </iframe>
                        </section>

                        <footer>
                            <p>© 2024 Остеопат Бикетова</p>
                            <ul>
                                <li><a href="https://vk.com/osteopat.biketova" target="_blank">ВКонтакте</a></li>
                                <li><a href="https://t.me/+dcXq8lbU7p05ZjNi" target="_blank">Telegram</a></li>
                                <li><a href="https://www.instagram.com/osteopat_biketova/" target="_blank">Instagram</a></li>
                                <li><a href="https://www.youtube.com/channel/UCxta34TZ-FLfosrG_AJCqAg" target="_blank">Youtube</a></li>
                            </ul>
                        </footer>
                        ]]>
                    </turbo:content>
                </item>
            </channel>
        </rss>
        """
        return HttpResponse(rss_content, content_type="application/rss+xml")
