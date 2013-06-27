from zope import interface, schema
from five import grok
from z3c.form.interfaces import HIDDEN_MODE
from plone.directives import form
from plone.supermodel.model import Schema
from plone.behavior import AnnotationStorage
from Products.CMFCore.utils import getToolByName
from collective.timelines.config import FONT_VOCAB, MAP_VOCAB
from collective.timelines import timelinesMessageFactory as _


class ITimelineSettings(Schema):
    """Form schema for timeline settings"""

    start_at_end = schema.Bool(
        title = _(u'Start at End of Timeline'))

    fonts = schema.Choice(
        title = _(u'Timeline Fonts'),
        required = True,
        default = u'Georgia-Helvetica',
        vocabulary=FONT_VOCAB)

    map_style = schema.Choice(
        title = _(u'Map Style'),
        required=True,
        default = u'ROADMAP',
        vocabulary=MAP_VOCAB)

TimelineStorage = AnnotationStorage(ITimelineSettings)


class TimelineConfigurationForm(form.SchemaEditForm):
    grok.name('timeline-configuration')
    grok.require('cmf.ModifyPortalContent')
    grok.context(interface.Interface)

    schema = ITimelineSettings
    label = _(u"Timeline Settings")
    description = _(u"Settings for timeline view")

    @property
    def has_maps_key(self):
        # Check for Products.Maps google map key
        properties = getToolByName(self.context, 'portal_properties')
        maps = getattr(properties, 'maps_properties', None)
        return bool(maps and getattr(maps, 'map_google_api_keys', None))

    def updateWidgets(self):
        super(TimelineConfigurationForm, self).updateWidgets()
        if not self.has_maps_key:
            self.widgets['map_style'].mode = HIDDEN_MODE
