import zope.interface
from Products.CMFPlone.tests import PloneTestCase

from Products.eeawebapplication.interface import IEEAWebApplication


class WebAppTestCase(PloneTestCase.PloneTestCase):
    
    def setupWebApp(self):
        zope.interface.directlyProvides(self.folder, IEEAWebApplication)
        self.workflow = self.portal.portal_workflow
        self.folder.invokeFactory('Folder', id='folder1', text='data', title='Foo2')
        self.folder.invokeFactory('Folder', id='folder2', text='data', title='Foo2')
        self.workflow.doActionFor(self.folder.folder1, 'publish')
        self.workflow.doActionFor(self.folder.folder2, 'publish')        

        self.folder.folder1.invokeFactory('Document', id='page1', text='data', title='Foo1')
        self.folder.folder2.invokeFactory('Document', id='page2', text='data', title='Foo2')        