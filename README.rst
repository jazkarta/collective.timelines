Introduction
============

This package which integrates the `Verite TimelineJS <http://timeline.verite.co/>`_
application into Plone.  Providing a beautiful, customizable timeline view
for folders and collections.

It adds a view ``timeline-view`` for Folders and new and old-style
(ATTopic) Collections (ATTopic).

In addition, it adds a Dexterity behavior for setting timeline dates
on content and a schema extender that applies to all Archetypes
content (except ATEvent, for which the normal date fields are used).

If the content has a remoteUrl (i.e. and ATLink), that link will be
used to generate the thumbnail for the page.  Special handling is
built in for Youtube, Twitter, Wikipedia and Flickr links, among
others.  Otherwise, the page url is used to generate the thumbnail.


Customizations
--------------

The default adapters for Archetypes and Dexterity content should
handle most usecases.  However, you may customize the timeline
metadata for specific content types by registering adapters to the
``ITimelineContent`` and/or ``ITimelineSupplement`` interfaces.

For example if I wanted to change the asset url for my IFoo content type
I would simply add the following to a grokked package::

    from five import grok
    from collective.timelines.interfaces import ITimelineSupplement

    class FooTimelineSupplement(grok.Adapter):
        grok.name('foo')
        grok.context(IFoo)
        grok.provides(ITimelineSupplement)

        def update(self, data):
            data['asset']['media'] = self.context.my_url
            return data

There is an example of a timeline supplement provided in the
map_support module, which uses metadata from ``Products.Maps`` enabled
content to display a map in the timeline.

To override the date calculation to use a custom date, or to
completely change the base data, you can override the ITimelineContent
adapter::

    from five import grok
    from DateTime import DateTime
    from collective.timelines.interfaces import ITimelineContent
    from collective.timelines.dexterity_content import TimeLineContent

    class FooTimelineContent(TimelineContent):
        grok.provides(ITimelineContent)
        grok.context(IFoo)

        def date(self):
            date = self.context.my_date
            return DateTime(date.year, date.month, date.day)

        def data(self):
            # Calculate custom dictionary for timeline date entry

There is an example of a custom ``ITimelineContent`` data provider in
the at_content module, which handles ATEvent content by automatically
using the start and end dates.
