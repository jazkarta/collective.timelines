Introduction
============

This package integrates the `Verite TimelineJS <http://timeline.verite.co/>`_
application into Plone, providing a beautiful, customizable timeline view
for folders and collections.

It adds a view ``timeline-view`` for Folders, new-style Collections, 
and old-style Collections (ATTopic).

In addition, it adds a Dexterity behavior for setting timeline dates
on content and a schema extender that applies to all Archetypes
content (except ATEvent, for which the normal date fields are used).

If the content has a remoteUrl (i.e. an ATLink), that link will be
used to generate the thumbnail for the page.  Special handling is
built in for Youtube, Twitter, Wikipedia and Flickr links, among
others.  Otherwise, the page url is used to generate the thumbnail.


Customizations
--------------

The default adapters for Archetypes and Dexterity content should
handle most use cases.  However, you may customize the timeline
metadata for specific content types by registering adapters to the
``ITimelineContent`` and/or ``ITimelineSupplement`` interfaces.


Note: Grok is no longer supported with Python 3. The examples below
need to be adapted to use `zcml` files.

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


Core Content Migration
----------------------

If you have extended ATCT content with this add-on and would like to preserve the data
when migrating to plone.app.contenttypes content, you will need to apply the dexterity
behavior `collective.timelines.dexterity_content.ITimelineBehavior` to the target
content types before migrating.

Credits
-------

* Alec Mitchell
* Carlos de la Guardia
* Jazkarta, Inc.
* With support and funding from `Dumbarton Oaks Research Library and Collection <http://doaks.org>`_, Washington DC
