""" AJAX Tabs
"""
import  zope.interface
from Acquisition import aq_inner
from App.special_dtml import DTMLFile
from Products.eeawebapplication.browser.interfaces import IAjaxTabs

class AjaxTabs(object):
    """ Class that activates ajax script for tabs
    """
    zope.interface.implements(IAjaxTabs)
    template = DTMLFile('www/ajaxtabs.js', globals())

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.tabListId = 'webapp-globalnav'
        self.tabPanelsId = 'content'

    def javascript(self, pages):
        """ Sets header to javascript for given pages
        """
        context = aq_inner(self.context)
        template = self.template.__of__(context)
        self.request.RESPONSE.setHeader('Content-Type',
                'application/x-javascript')
        self.request.RESPONSE.write( template( tabs = pages,
            tabListId = self.tabListId, tabPanelsId = self.tabPanelsId) )
