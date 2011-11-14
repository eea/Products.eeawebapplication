#
# Tests the Main view
#

import zope.interface

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Products.CMFPlone.tests import PloneTestCase
from Products.eeawebapplication.browser.convert import Convert
from Products.eeawebapplication.interface import IEEAWebApplication

class TestConvertView(PloneTestCase.PloneTestCase):

    def afterSetUp(self):
        self.url = self.portal.portal_url
        
    def testMakeWebApp(self):
        self.setRoles(['Manager'])
        view = Convert(self.folder, self.app.REQUEST)
        view.makeWebApp()
        provided = zope.interface.directlyProvidedBy(self.folder)
        self.failIf(IEEAWebApplication not in provided)

        view.removeWebApp()
        provided = zope.interface.directlyProvidedBy(self.folder)
        self.failIf(IEEAWebApplication in provided)
 
def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestConvertView))
    return suite

if __name__ == '__main__':
    framework()
