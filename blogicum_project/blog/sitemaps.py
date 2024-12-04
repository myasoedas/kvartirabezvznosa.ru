from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

class StaticViewSitemap(Sitemap):
    """Карта сайта для статических страниц."""
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        """Возвращает имена маршрутов, которые включаются в карту сайта."""
        return ['blog:index', 'blog:robots_txt', 'blog:rss_feed']

    def location(self, item):
        """Генерирует URL для каждого маршрута."""
        return reverse(item)

