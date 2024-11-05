# blogicum/blog/views.py
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
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


class CommentDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'

    def get_success_url(self):
        return reverse('blog:post_detail',
                       kwargs={'post_id': self.object.post.id})


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/create.html'
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return reverse('blog:index')

    def handle_no_permission(self):
        return HttpResponseRedirect(self.get_object().get_absolute_url())


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


class PostEditView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/create.html'
    fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']
    pk_url_kwarg = 'post_id'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def handle_no_permission(self):
        return redirect(self.get_object().get_absolute_url())


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text', 'image', 'category', 'location', 'pub_date']
    template_name = 'blog/create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:profile',
                       kwargs={'username': self.request.user.username})


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
