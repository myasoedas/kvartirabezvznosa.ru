from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone

from .constants import NUMBER_OF_POSTS
from .models import Post


class PostQueryMixin:
    def get_filtered_posts(self, author=None, published_only=False):
        queryset = Post.objects.select_related(
            'author', 'category', 'location')
        if author:
            queryset = queryset.filter(author=author)
        if published_only:
            queryset = queryset.filter(
                is_published=True,
                pub_date__lte=timezone.now(),
                category__is_published=True
            )
        return queryset.annotate(
            comment_count=Count('comments')).order_by('-pub_date')


class AuthorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return self.request.user == obj.author


class PostCommentCountMixin:
    def add_comment_count(self, posts):
        return posts.annotate(comment_count=Count('comments'))


class PaginatorMixin:
    paginate_by = NUMBER_OF_POSTS

    def get_paginated_context(self, queryset):
        paginate_by = self.paginate_by or NUMBER_OF_POSTS
        paginator = Paginator(queryset, paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return {
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
        }
