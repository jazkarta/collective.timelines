from zope import interface
from Products.Maps.interfaces import IGeoLocation
from collective.timelines.interfaces import ITimelineSupplement


MAP_BASE = 'http://maps.google.com/maps?f=q&q=%s,%s'

class MapTimlineUpdater(object):
    interface.implements(ITimelineSupplement)

    def __init__(self, context):
        self.context = context

    def update(self, data):
        context = self.context
        coords = IGeoLocation(context, None)
        if coords and coords.latitude and coords.longitude:
            data['asset']['media'] = MAP_BASE%(coords.latitude,
                                               coords.longitude)
