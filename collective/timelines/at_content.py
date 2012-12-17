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
                                    label=_(u'Use Publication Date(s)')),
                       ),
        ExtensionDateTimeField('timeline_date',
                               schemata='Timeline Config',
                               widget = CalendarWidget(
                                    label=_(u'Custom Timeline Date')),
                        ),
        ExtensionDateTimeField('timeline_end',
                               schemata='Timeline Config',
                               widget = CalendarWidget(
                                    label=_(u'Timeline End Date')),
                        ),
        ExtensionBooleanField('bce_year',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Year is BCE')),
                       ),
        ExtensionBooleanField('year_only',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Display year only on timeline')),
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

    def end(self):
        context = self.context
        if not context.getField('timeline_end'):
            # Schema not extended
            return
        if context.getField('use_pub_date').get(context):
            return context.getExpirationDate()
        return context.getField('timeline_end').get(context)

    def _get_image_url(self):
        context = self.context
        field = context.getField('image')
        if field is not None:
            image = (field.getScale(context, scale='preview') or
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

        if ignore_date and context.getField('text'):
            # Use text field instead of description on primary item
            text = context.getField('text').get(context)
            # Avoid weird auto-twitter logic
            text = text.replace('/@@images/', '/images/')
            data['text'] = text or data['text']

        if not ignore_date:
            date = self.date()
            if not date:
                return
            bce_field = context.getField('bce_year')
            bce = bce_field and bce_field.get(context)
            year_only_field = context.getField('year_only')
            year_only = year_only_field and year_only_field.get(context)
            data['startDate'] = format_datetime(date, year_only)
            if bce:
                data['startDate'] = '-' + data['startDate']
            end = self.end()
            if end:
                data['endDate'] = format_datetime(end, year_only)
                if bce:
                    data['endDate'] = '-' + data['endDate']

        subject = context.Subject()
        if subject:
            # Take the first keyword, somewhat arbitrarily
            data['tag'] = subject[0]

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

    def end(self):
        context = self.context
        return context.getField('endDate').get(context)

    def data(self, ignore_date=False):
        data = super(EventTimelineContent, self).data(ignore_date)
        context = self.context
        if not ignore_date:
            data['endDate'] = format_datetime(context.getField('endDate').get(
                context))
        return data
