"""Blog Listing and blog detail pages"""

from django.db import models
from django.shortcuts import render

from modelcluster.fields import ParentalKey

from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page, Orderable
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, StreamFieldPanel
from wagtail.core.fields import StreamField
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail.snippets.edit_handlers import SnippetChooserPanel


from streams import blocks

# Create your models here.


class BlogAuthorsOrderable(Orderable):
    """This allow us to select one or more blog authors from a list taken from snippets"""
    page = ParentalKey("blog.BlogDetailPage", related_name="blog_authors")
    author = models.ForeignKey(
        "blog.BlogAuthor",
        on_delete=models.CASCADE,

    )
    panels = [
        SnippetChooserPanel("author")
    ]


class BlogAuthor(models.Model):
    """Blog Author for snippets."""
    name = models.CharField(max_length=100)
    website = models.URLField(blank=True, null=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="+"
    )
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("name"),
                ImageChooserPanel("image")
            ],
            heading="Name and Image"
        ),
        MultiFieldPanel(
            [
                FieldPanel("website"),
            ],
            heading="Links"
        ),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Blog Author"
        verbose_name_plural = "Blog Authors"


register_snippet(BlogAuthor)


class BlogListingPage(RoutablePageMixin, Page):
    """Listing page lists all the Blog Detail Pages"""

    custom_title = models.CharField(
        max_length=100, blank=False, null=False, help_text='Overwrites the default title')

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context"""
        context = super().get_context(request, *args, **kwargs)
        context["posts"] = BlogDetailPage.objects.live().public()
        context["authors"] = BlogAuthor.objects.all()
        context["a_special_link"] = self.reverse_subpage('latest_post')
        return context

    @route(r'latest/$', name="latest_post")
    def latest_blog_posts(self, request, *args, **kwargs):
        context = self.get_context(request, *args, **kwargs)
        context["latest_posts"] = BlogDetailPage.objects.live().public()[:1]
        return render(request, "blog/latest_posts.html", context)

    def get_sitemap_urls(self, request):
        # uncomment si no queremos que figure en el sitemap
        # return []
        sitemap = super().get_sitemap_urls(request)
        sitemap.append({
            "location": self.full_url + self.reverse_subpage("latest_post"),
            "lastmod": (self.last_published_at or self.latest_revision_created_at),
            "priority": 0.9
        })
        return sitemap

    template = "blog/blog_listing_page.html"


class BlogDetailPage(Page):
    """Blog detail page"""

    custom_title = models.CharField(
        max_length=100, blank=False, null=False, help_text='Overwrites the default title')

    blog_image = models.ForeignKey(
        "wagtailimages.Image", blank=False, null=True, related_name="+", on_delete=models.SET_NULL)

    content = StreamField(
        [
            ("title_and_text", blocks.TitleAndTextBlock()),
            ("full_richtext", blocks.RichTextBlock()),
            ("simple_richtext", blocks.SimpleRichTextBlock()),
            ("cards", blocks.CardBlock()),
            ("cta", blocks.CTABlock()),
        ],
        null=True,
        blank=True
    )

    content_panels = Page.content_panels + [
        FieldPanel("custom_title"),
        ImageChooserPanel("blog_image"),
        MultiFieldPanel([
            InlinePanel("blog_authors", label="Author", min_num=1, max_num=4)
        ], heading="Author(s)"),
        StreamFieldPanel("content"),
    ]
