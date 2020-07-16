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
        if not ITimelineBehavior.providedBy(new):
            return
        migrate_simplefield(old, new, 'use_pub_date', 'use_pub_date')
        migrate_datetimefield(old, new, 'timeline_date', 'timeline_date')
        migrate_datetimefield(old, new, 'timeline_end', 'timeline_end')
        migrate_simplefield(old, new, 'bce_year', 'bce_year')
        migrate_simplefield(old, new, 'year_only', 'year_only')
        migrate_simplefield(old, new, 'show_tag', 'show_tag')
