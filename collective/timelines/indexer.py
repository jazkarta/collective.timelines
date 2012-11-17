from five import grok
from zope.component import queryAdapter
from plone.indexer import indexer
from collective.timelines.interfaces import ITimelineContent
from Products.CMFCore.interfaces import IDynamicType


@indexer(IDynamicType)
def timelineDate(obj):
    adapter = queryAdapter(obj, ITimelineContent)
    return adapter and adapter.date() or None
grok.global_adapter(timelineDate, name='timeline_date')
