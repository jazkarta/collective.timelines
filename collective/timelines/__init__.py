import xml.etree.ElementTree as ET
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
    return '%s,%s,%s'%(date.year(),date.month(),date.day())

def get_image_url(context, size='large'):
    # Look at the imaging view
    request = getattr(context, 'REQUEST', None)
    if request is not None:
        image_view = getMultiAdapter((context, request),
                                     name='images')
        try:
            scale_attr = size and [size] or []
            image = image_view.traverse('image', scale_attr)
            if image:
                # This returns an image tag, pull the src attribute
                return ET.fromstring(image).attrib['src']
        except (AttributeError, TraversalError):
            if IImageContent.providedBy(context):
                image = context.getImage()
                if image:
                    return image.absolute_url()
            if hasattr(context, 'getField'):
                field = context.getField('image')
                handler = IImageScaleHandler(field, None)
                if handler is not None:
                    image = handler.getScale(context, size)
                    if image:
                        return image.absolute_url()
