from zope.i18nmessageid import MessageFactory


timelinesMessageFactory = MessageFactory('collective.timelines')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

def format_datetime(date):
    return '%s,%s,%s'%(date.year(),date.month(),date.day())
