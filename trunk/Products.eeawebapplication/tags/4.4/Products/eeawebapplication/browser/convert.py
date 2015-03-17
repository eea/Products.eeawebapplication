""" Convert
"""
import zope.interface
from Products.Five.browser import BrowserView
from Products.eeawebapplication.interface import IEEAWebApplication

class Convert(BrowserView):
    """ Browser View that implements methods to make webapp from folder
    """

    def makeWebApp(self):
        """ Make folder webapp by providing IEEAWebApplication interface
        """
        currentInterfaces = zope.interface.directlyProvidedBy(self.context)
        zope.interface.directlyProvides(self.context,
                                        currentInterfaces,
                                        IEEAWebApplication)

    def removeWebApp(self):
        """ Remove webbapp interface from folder.
        """
        currentInterfaces = zope.interface.directlyProvidedBy(self.context)
        newInterfaces = currentInterfaces - IEEAWebApplication
        zope.interface.directlyProvides(self.context, newInterfaces)

