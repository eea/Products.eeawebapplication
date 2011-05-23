""" Interfaces
"""
from zope.interface import Interface

class IWebAppView(Interface):
    """ IWebAppView interface
    """

    def menu():
        """ Returns info for the main tabs.
        """

    def submenu():
        """ Returns info for sub menu for the current page.
        """

    def ajax():
        """ Returns the Javascript to register and preload pages.
        """

class IAjaxTabs(Interface):
    """ generate javascript for the tabs from the content in a webapp
    """

    def javascript():
        """ Generate javascript for the ajax tabs.
        """
