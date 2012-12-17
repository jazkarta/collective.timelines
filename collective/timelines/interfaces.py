from zope.interface import Interface

class ITimelineContent(Interface):

    def date():
        """Returns the timeline date (DateTime) for the content"""

    def end():
        """Returns the timeline date (DateTime) for the content"""

    def data(ignore_date=False):
        """Returns data structure for verite timeline JSON date entry,
        skips checking/including start data if ``ignore_date`` is
        enabled"""


class ITimelineSupplement(Interface):

    def update(data):
        """Updates timeline data with additional configuration"""
