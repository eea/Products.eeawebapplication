""" Tests the Main view
"""
from Products.eeawebapplication.tests.base import WebAppTestCase
from Products.eeawebapplication.browser.main import Main, PrepareBody
from unittest import TestSuite, makeSuite

class TestMainView(WebAppTestCase):
    """ Main Test class
    """

    def afterSetUp(self):
        """ after setup method of test case
        """
        self.url = self.portal.portal_url
        self.setupWebApp()

    def testSelectedTabs(self):
        """ test selected tabs
        """
        self.setRoles(['Manager'])
        view = Main(self.folder.folder1, self.app.REQUEST)
        result = view.menu()
        for menu in result:
            if menu['id'] == 'folder1':
                self.failIf(menu['class'] != 'selected')

    def testRelativUrlFix(self):
        """ test relative url fix
        """
        body = 'Some text with <a href="local-url">local</a> link and some' \
               '<a href="../relative1">relative1</a>' \
               'and a <a href="/absolute">absolute link</a> too. Why not a' \
               '<a href="../folder2_ff/relative2-url">relative2</a>'
        answer = 'Some text with <a href="folder1/local-url">local</a> link' \
                ' and some<a href="relative1">relative1</a>and a ' \
                '<a href="/absolute">absolute link</a> too. Why not a' \
                '<a href="folder2_ff/relative2-url">relative2</a>'
        page = self.folder.folder1.page1
        view = PrepareBody(page, self.app.REQUEST)
        result =  view.fixLinks(body)
        self.failIf(answer != result, result)

def test_suite():
    """ test suite
    """
    suite = TestSuite()
    suite.addTest(makeSuite(TestMainView))
    return suite
