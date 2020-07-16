import re
from zope.component import adapts
from zope.interface import implements
from DateTime import DateTime
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from Products.Archetypes.atapi import (BooleanField, DateTimeField,
                                       BooleanWidget, StringWidget,)
from Products.Archetypes.interfaces import IBaseContent
from Products.ATContentTypes.interfaces import IATEvent
from Products.CMFCore.utils import getToolByName
from collective.timelines.interfaces import ITimelineContent
from collective.timelines import (timelinesMessageFactory as _,
                                  format_datetime,
                                  get_image_url,)

YEAR_ONLY = re.compile('^\d+$')

class ExtensionBooleanField(ExtensionField, BooleanField):
    pass

class ExtensionDateTimeField(ExtensionField, DateTimeField):

    def set(self, instance, value, **kwargs):
        # Add some custom date parsing to ensure pre-year-1000 dates
        # are handled well, and allow standalone years
        if value and isinstance(value, basestring):
            if '/' in value:
                # convert / to -, to force better parsing
                value.replace('/', '-')
            elif YEAR_ONLY.match(value):
                value = '%04d-01-01'%(int(value))
            value = DateTime(value)
        super(ExtensionDateTimeField, self).set(instance, value,
                                                **kwargs)

    def getRaw(self, instance, **kwargs):
        value = super(ExtensionDateTimeField, self).getRaw(instance, **kwargs)
        if isinstance(value, DateTime):
            return '%04d-%02d-%02d'%(value.year(),value.month(),value.day())
        return value

class TimelineExtender(object):
    adapts(IBaseContent)
    implements(ISchemaExtender)

    fields = [
        ExtensionBooleanField('use_pub_date',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Use Publication Date(s)'),
                                    visible= {'view': 'invisible'},),
                       ),
        ExtensionDateTimeField('timeline_date',
                               schemata='Timeline Config',
                               widget = StringWidget(
                                    label=_(u'Custom Timeline Date'),
                                    description=_(
        u'Must be entered as "YYYY-MM-DD" or a standalone year (e.g. "0525-02-23" or "25" for year 25)'),
                                    visible= {'view': 'invisible'},)
                        ),
        ExtensionDateTimeField('timeline_end',
                               schemata='Timeline Config',
                               widget = StringWidget(
                                    label=_(u'Timeline End Date'),
                                    description=_(
        u'Must be entered as "YYYY-MM-DD" or a standalone year (e.g. "0525-02-23" or "25" for year 25)'),
                                    visible= {'view': 'invisible'},)
                        ),
        ExtensionBooleanField('bce_year',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Year is BCE'),
                                    visible= {'view': 'invisible'},),
                       ),
        ExtensionBooleanField('year_only',
                              schemata='Timeline Config',
                              widget = BooleanWidget(
                                    label=_(u'Display year only on timeline'),
                                    visible= {'view': 'invisible'},),
                       ),
        ExtensionBooleanField('show_tag',
                              schemata='Timeline Config',
                              default=False,
                              widget = BooleanWidget(
                                label=_(u'Show first tag in timeline'),
                                visible= {'view': 'invisible'},),
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
        show_tag = context.getField('show_tag')
        if subject and (show_tag is not None) and show_tag.get(context):
            # Take the first keyword, somewhat arbitrarily
            data['tag'] = subject[0]

        data['asset'] = {}
        # Links
        if context.getField('remoteUrl'):
            data['asset']['media'] = context.getField('remoteUrl').get(context)
        elif not ignore_date:
            # Include a url to the content
            url = context.absolute_url()
            site_properties = getattr(
                getToolByName(context, 'portal_properties'), 'site_properties', None
            )
            registry = getToolByName(self.context, 'portal_registry')
            view_types = (
                getattr(site_properties, 'typesUseViewActionInListings', None) or
                registry.get('plone.types_use_view_action_in_listings', ())
            )
            if context.portal_type in view_types:
                url = url + '/view'
            data['text'] = (data['text'] +
                            ' <a href="%s">more &hellip;</a>' % url)

        image_url = get_image_url(self.context)
        # Items with Images
        if image_url:
            data['asset']['thumbnail'] = get_image_url(self.context, 'icon')
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
