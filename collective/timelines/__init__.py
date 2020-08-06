from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.traversing.interfaces import TraversalError
from Products.ATContentTypes.interfaces import IImageContent
from plone.app.imaging.interfaces import IImageScaleHandler


timelinesMessageFactory = MessageFactory('collective.timelines')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

def format_datetime(date, year_only=False):
    if year_only:
        return str(date.year())
    return '%s,%s,%s,%s,%s'%(date.year(),date.month(),date.day(),date.hour(),date.minute())

def get_image_url(context, size='large'):
    # Look at the imaging view
    request = getattr(context, 'REQUEST', None)
    if request is not None:
        image_view = getMultiAdapter((context, request),
                                     name='images')
        # compatibility with collective.contentleadimage
        image_url = None
        for image_name in ['image', 'leadImage']:
            try:
                scale = image_view.scale(fieldname=image_name, scale=size)
                if scale is not None:
                    image_url = scale.url
            except (AttributeError, TraversalError):
                if IImageContent.providedBy(context):
                    image = context.getImage()
                    if image:
                        image_url = image.absolute_url()
                if hasattr(context, 'getField'):
                    field = context.getField('image')
                    handler = IImageScaleHandler(field, alternate=None)
                    if handler is not None:
                        image = handler.getScale(context, size)
                        if image:
                            image_url = image.absolute_url()
        # The library seems to prefer http urls
        return image_url
