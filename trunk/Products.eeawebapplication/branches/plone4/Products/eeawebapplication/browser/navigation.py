""" Module which implements a custom renderer for the portlet navigation
"""
import zope.interface

from Acquisition import aq_base
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import INavigationPortlet
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.portlets.portlets import navigation
from Products.eeawebapplication.interface import IEEAWebApplication
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy

def getApplicationRoot(obj):
    """ Returns root of application for given object """
    portal_url = getToolByName(obj, 'portal_url')
    portal = portal_url.getPortalObject()

    while not IEEAWebApplication.providedBy(obj) and aq_base(obj) \
                                            is not aq_base(portal):
        obj = utils.parent(obj)

    return obj

class ApplicationNavigationPortlet(navigation.Renderer):
    """ EEA website can have IEEAWebApplication roots. """

    zope.interface.implements(INavigationPortlet)

    def title(self):
        """ Returns title of root container. """
        root = self.getNavRoot()
        return root.Title()

    def getNavRoot(self):
        """ Override """
        if not utils.base_hasattr(self, '_root'):
            self._root = [ getApplicationRoot( utils.context(self) ) ]
        return self._root[0]

class ApplicationNavtreeStrategy(DefaultNavtreeStrategy):
    """ The navtree strategy used for the default navigation portlet and
        respects IEEAWebApplication root.  """

    zope.interface.implements(INavtreeStrategy)

    def __init__(self, context, view=None):
        DefaultNavtreeStrategy.__init__(self, context, view)
        self.rootPath = '/'.join(getApplicationRoot(context).getPhysicalPath())

