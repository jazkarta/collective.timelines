import json
from zope.component import getMultiAdapter, getAdapters
from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from collective.timelines.interfaces import (ITimelineContent,
                                             ITimelineSupplement)
from collective.timelines.browser.configuration import ITimelineSettings
from Products.CMFCore.utils import getToolByName


class TimelineView(BrowserView):
    """A view providing timeline settings data"""

    @property
    def start_at_end(self):
        return (ITimelineSettings(self.context).start_at_end and
                'true' or 'false')

    @property
    def font(self):
        return ITimelineSettings(self.context).fonts

    @property
    def map_style(self):
        return ITimelineSettings(self.context).map_style

    @property
    def data_url(self):
        return '{}/@@timeline-json'.format(
            self.context.absolute_url().rstrip('/')
        )

    @property
    def resource_base(self):
        return (getToolByName(self.context, 'portal_url')() +
                '/++resource++timelines')

    @property
    def lang(self):
        context = aq_inner(self.context)
        portal_state = getMultiAdapter((context, self.request),
                                       name=u'plone_portal_state')
        return portal_state.language() or 'en'


class TimelineFolderJSON(BrowserView):
    """JSON Representation of folder contents"""

    def __call__(self):
        """test render"""
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(self.content_data())

    def _get_contents(self):
        context = aq_inner(self.context)
        return context.listFolderContents()

    def content_data(self):
        """Return JSON representation of timeline contents"""
        context = aq_inner(self.context)
        base_data = {"timeline": {"type":"default",
                                  "date": []}}
        data = ITimelineContent(context).data(ignore_date=True)
        base_data['timeline'].update(data)
        contents = self._get_contents()
        dates = base_data['timeline']['date']
        for item in contents:
            item_data = ITimelineContent(item).data()
            if not item_data:
                continue
            updaters = getAdapters((item,), ITimelineSupplement)
            # Sort by name
            for name, updater in sorted(updaters):
                updater.update(item_data)

            dates.append(item_data)

        return base_data


class TimelineTopicJSON(TimelineFolderJSON):
    """JSON representation of topic contents"""

    def _get_contents(self):
        context = aq_inner(self.context)
        # Filter query on content with a timeline date set
        return context.queryCatalog(batch=False, full_objects=True,
                                    sort_on='timeline_date')

class TimelineCollectionJSON(TimelineFolderJSON):
    """JSON representation of topic contents"""

    def _get_contents(self):
        context = aq_inner(self.context)
        # Filter query on content with a timeline date set
        return context.results(batch=False, brains=False,
                               sort_on='timeline_date')
