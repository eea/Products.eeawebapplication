import zope.interface

from Acquisition import aq_base, aq_inner
from Products.CMFPlone import utils
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.interfaces import INavigationPortlet, INavtreeStrategy
from Products.CMFPlone.browser.portlets.navigation import NavigationPortlet
from Products.eeawebapplication.interface import IEEAWebApplication
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy

def getApplicationRoot(obj):
    portal_url = getToolByName(obj, 'portal_url')	    
    portal = portal_url.getPortalObject()
        
    while not IEEAWebApplication.providedBy(obj) and aq_base(obj) is not aq_base(portal):
        obj = utils.parent(obj)
            
    return obj

class ApplicationNavigationPortlet(NavigationPortlet):
    """ EEA website can have IEEAWebApplication roots. """
    
    zope.interface.implements(INavigationPortlet)

    def title(self):
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

