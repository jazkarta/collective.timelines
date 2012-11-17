from Products.CMFCore.utils import getToolByName

VIEW_TYPES = ('Folder', 'Topic', 'Collection')


def revert_type_actions(context):
    if context.readDataFile('remove_types.txt') is None:
        return
    portal = context.getSite()
    ptypes = getToolByName(portal, 'portal_types')
    for t in VIEW_TYPES:
        if t not in ptypes.objectIds():
            continue
        fti = ptypes[t]
        for i,action in enumerate(fti.listActions()):
            if action.id == 'timeline-configuration':
                fti.deleteActions((i,))
                break

