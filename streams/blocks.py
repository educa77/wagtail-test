"""Streamfields live in here"""

from wagtail.core import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    """Title and text and nothing else"""

    title = blocks.CharBlock(required=True, help_text='Add your title')
    text = blocks.TextBlock(required=True, help_text='Add additional text')

    class Meta:
        template = "streams/title_and_text_block.html"
        icon = 'edit'
        label = 'Title & Text'


class RichTextBlock(blocks.RichTextBlock):
    """richtext with all the features"""

    class Meta:
        template = "streams/richtext_block.html"
        icon = 'doc-full'
        label = 'Full RichText'


class SimpleRichTextBlock(blocks.RichTextBlock):
    """richtext with limited features"""

    def __init__(
        self, required=True, help_text=None, editor="default", features=None, **kwargs
    ):  # noqa
        super().__init__(**kwargs)
        self.features = ["bold", "italic", "link"]

    class Meta:
        template = "streams/richtext_block.html"
        icon = 'edit'
        label = 'Simple RichText'


class CardBlock(blocks.StructBlock):
    """card with image and text"""
    title = blocks.CharBlock(required=True, help_text='Add your title')
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("image", ImageChooserBlock(required=True)),
            ("title", blocks.CharBlock(require=True, max_length=40)),
            ("text", blocks.TextBlock(required=True, max_length=200)),
            ("button_page", blocks.PageChooserBlock(required=False)),
            ("button_url", blocks.URLBlock(required=False,
             help_text="If the button above is selected, that will be used first")),

        ])
    )

    class Meta:
        template = "streams/card_block.html"
        icon = 'placeholder'
        label = 'Staff Cards'


class CTABlock(blocks.StructBlock):
    """A simpole call to action"""
    title = blocks.CharBlock(required=True, max_length=60)
    text = blocks.RichTextBlock(required=True, features=["bold", "italic"])
    button_page = blocks.PageChooserBlock(required=False)
    button_url = blocks.URLBlock(required=False)
    button_text = blocks.CharBlock(
        required=True, default='Learn More', max_length=40)

    class Meta:
        template = "streams/cta_block.html"
        icon = 'placeholder'
        label = 'Call to Action'
