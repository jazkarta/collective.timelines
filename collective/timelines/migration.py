from zope.component import adapter
from zope.interface import implementer
from plone.app.contenttypes.migration.migration import ICustomMigrator, BaseCustomMigator
from plone.app.contenttypes.migration.field_migrators import migrate_simplefield
from plone.app.contenttypes.migration.field_migrators import migrate_datetimefield
from Products.Archetypes.interfaces import IBaseContent

from .dexterity_content import ITimelineBehavior


@implementer(ICustomMigrator)
@adapter(IBaseContent)
class ITimelineDataMigrator(BaseCustomMigator):

    def migrate(self, old, new):
        adapted = ITimelineBehavior(new, alternate=None)
        if adapted is None:
            return
        migrate_simplefield(old, adapted, 'use_pub_date', 'use_pub_date')
        # Timeline dates are always naive
        if old.getField('timeline_date').get(old):
            migrate_datetimefield(old, adapted, 'timeline_date', 'timeline_date')
            if adapted.timeline_date:
                adapted.timeline_date = adapted.timeline_date.replace(tzinfo=None)
        if old.getField('timeline_end').get(old):
            migrate_datetimefield(old, adapted, 'timeline_end', 'timeline_end')
            if adapted.timeline_end:
                adapted.timeline_end = adapted.timeline_end.replace(tzinfo=None)
        migrate_simplefield(old, adapted, 'bce_year', 'bce_year')
        migrate_simplefield(old, adapted, 'year_only', 'year_only')
        migrate_simplefield(old, adapted, 'show_tag', 'show_tag')
