from zope.component import adapts, getMultiAdapter
from zope.interface import implements
from zope.traversing.interfaces import TraversalError
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import (BooleanField, DateTimeField,
                                       BooleanWidget, CalendarWidget,)
from Products.Archetypes.interfaces import IBaseContent
from Products.ATContentTypes.interfaces import IATEvent, IImageContent
from collective.timelines.interfaces import ITimelineContent
from collective.timelines import timelinesMessageFactory as _, format_datetime

class ExtensionBooleanField(ExtensionField, BooleanField):
    pass

class ExtensionDateTimeField(ExtensionField, DateTimeField):
    pass

class TimelineExtender(object):
    adapts(IBaseContent)
    implements(ISchemaExtender)

    fields = [
        ExtensionBooleanField('use_pub_date',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Use Publication Date')),
                       ),
        ExtensionDateTimeField('timeline_date',
                               schemata='Timeline Config',
                               widget = CalendarWidget(
                                    label=_(u'Custom Timeline Date')),
                        ),
        ExtensionBooleanField('bce_year',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Year is BCE')),
                       ),
        ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        # Don't add fields for events
        if IATEvent.providedBy(self.context):
            return []
        return self.fields


class TimelineContent(object):
    adapts(IBaseContent)
    implements(ITimelineContent)

    def __init__(self, context):
        self.context = context

    def date(self):
        context = self.context
        if not context.getField('timeline_date'):
            # Schema not extended
            return
        if context.getField('use_pub_date').get(context):
            return context.getEffectiveDate()
        return context.getField('timeline_date').get(context)

    def _get_image_url(self):
        context = self.context
        field = context.getField('image')
        if field is not None:
            image = (field.getScale(context, scale='mini') or
                     field.getScale(context))
            if image:
                return image.absolute_url()
        elif IImageContent.providedBy(context):
            image = context.getImage()
            if image:
                return image.absolute_url()

    def data(self, ignore_date=False):
        context = self.context
        data = {"headline": context.Title(),
                "text": "<p>%s</p>"%context.Description(),}

        if not ignore_date:
            date = self.date()
            if not date:
                return
            data['startDate'] = format_datetime(date)
            bce_field = context.getField('bce_year')
            if bce_field and bce_field.get(context):
                data['startDate'] = '-' + data['startDate']

        subject = context.Subject()
        if subject:
            data['tag'] = ', '.join(subject)

        data['asset'] = {}
        # Links
        if context.getField('remoteUrl'):
            data['asset']['media'] = context.getField('remoteUrl').get(context)
        elif not ignore_date:
            # Include a url to the content
            data['text'] = (data['text'] +
                    ' <a href="%s">more &hellip;</a>'%context.absolute_url())

        image_url = self._get_image_url()
        # Items with Images
        if image_url:
            data['asset']['thumbnail'] = image_url
            if 'media' not in data['asset']:
                data['asset']['media'] = image_url

        # News-like items
        if 'asset' in data and context.getField('imageCaption'):
            data['asset']['caption'] = (
                context.getField('imageCaption').get(context)
                )
        # TODO: Asset 'credit'?

        return data


class EventTimelineContent(TimelineContent):
    adapts(IATEvent)
    implements(ITimelineContent)

    def date(self):
        context = self.context
        return context.getField('startDate').get(context)

    def data(self, ignore_date=False):
        data = super(EventTimelineContent, self).data(ignore_date)
        context = self.context
        if not ignore_date:
            data['endDate'] = format_datetime(context.getField('endDate').get(
                context))
        return data
