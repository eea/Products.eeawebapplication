################################################################################
# Copyright (C) 2006  EEA - European Enviromental Agency
# 			    Antonio De Marinis <antonio.de.marinis@eea.eu.int> 
#                    Sasha Vincic <sasha.vincic@lovelysystems.com>
#                    
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.
################################################################################

"""
$Id$
"""

import  zope.interface
import zope.component

import re
from zope.app.basicskin.standardmacros import Macros
from Acquisition import aq_base, aq_inner, aq_parent
from App.special_dtml import DTMLFile

from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils as putils
from Products.eeawebapplication.interface import IEEAWebApplication
import logging

logger = logging.getLogger('Products.eeawebapplication.browser.main')
AjaxTabs = None
try:
    from Products.ptabs.ajaxtabs.ajaxtabs import AjaxTabs
except ImportError, err:
    logger.debug(err)

from interfaces import IWebAppView

class StandardMacros(BrowserView, Macros):
    """ StandardMacros BrowserView with main_template. """
    macro_pages = ('main_template','menu')

# Format strings into something that can be parsed as
# javascript.  Be warned that this logic right now is quite
# fragile (ie doesn't take into account non-ascii chars, etc)...
# but previously didn't take care of newlines - Rocky
def js_format(orig):
    formatted = ''
    for c in orig:
        if c == "\r":
            c = ''
        elif c == "\n":
            c = "\\n"
        elif c == "'":
            c = "\\'"
        elif c == "?":
            c = "\\?"
        formatted += c
    return formatted

class Main(BrowserView):
    """ Main BrowserView for Products.eeawebapplication. """
    zope.interface.implements(IWebAppView)

    def _setCacheHeaders(self):
        """ Set cache headers. """
        self.request.RESPONSE.setHeader('Cache-Control',
                        'max-age=0, s-maxage=3600, must-revalidate')

    def test(self, variable, trueValue, falseValue):
        """ Tests if variable is assigned & returns trueValue or falseValue. """
        if variable:
            return trueValue
        else:
            return falseValue

    def home(self):
        """ Returns absolute_url of root. """
        root = self._getRoot()
        return root.absolute_url()

    def menu(self):
        """ Constructs menu for root folders. """
        tabs = self.pages()
        menu = []

        currentUrl = self.context.absolute_url()
        for tab in tabs:
            cssClass = 'plain'
            checkUrl = not currentUrl == self.home()
            if checkUrl and tab.getURL() in currentUrl:
                cssClass = 'selected'
            tabId = tab.getId.replace('-','_')
            cxId =  self.context.getId().replace('-','_')
            onClick  = "javascript:tabs%s.OpenTab" \
                    "('subportaltab_%s','%s','%s/subbody', false, '');" % \
                    (cxId, tabId, js_format(tab.Title), tab.getURL())
            menu.append( {'id': tab.getId,
                    'tabId': tabId,
                    'title': tab.Title,
                    'url': '%s' % tab.getURL(),
                    'description': tab.Description,
                    'class': cssClass,
                    'onclick': onClick })
        return menu

    def getDefaultPageId(self):
        """ Returns default page id. """
        cId = self.context.getId()
        root = self._getRoot()
        if hasattr(root, cId) and root.getId() != cId:
            return cId
        else:
            return self.pages()[0].getId

    def _getRoot(self):
        """ Return the root of our application. """
        if not putils.base_hasattr(self, '_root'):
            portal_url = getToolByName(self.context, 'portal_url')
            portal = portal_url.getPortalObject()
            obj = self.context
            while not IEEAWebApplication.providedBy(obj) and aq_base(obj) \
                                                    is not aq_base(portal):
                obj =  aq_parent(aq_inner(obj))
            self._root = [obj]
        return self._root[0]

    def pages(self):
        """ Return query of published folders.  """
        catalog = getToolByName(self.context, 'portal_catalog')
        obj = self._getRoot()
        query = {}
        query['path'] =  {'query' : '/'.join(obj.getPhysicalPath()),
                     'depth' : 1 }
        query['portal_type'] = 'Folder'
        query['review_state'] = 'published'

        portal_properties = getToolByName(self.context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        result = catalog.searchResults(query)
        return result

    template = DTMLFile('www/ajaxtabs.js', globals())
    template_main = DTMLFile('www/mainajaxtabs.js', globals())

    def javascript(self):
        """ Ajaxifies root tabs. """
        tabs = AjaxTabs(self.context, self.request)
        tabs.tabListId = 'webapp-globalnav'
        tabs.tabPanelsId = 'content'
        context = aq_inner(self.context)
        template = self.template.__of__(context)
        template_main = self.template_main.__of__(context)
        menu = self.menu()
        for m in menu:
            folder = getattr(self.context, m['id'], None)
            if folder:
                defaultPage = folder.getDefaultPage()
                if defaultPage:
                    m['url'] = '%s/%s' % (m['url'], defaultPage)
            m['id'] = m['tabId']

        menu = self.menu()
        submenuJS = ''
        for m in menu:
            folder = getattr(self.context, m['id'], None)
            if folder:
                submenu = SubMenu(folder, self.request)
                submenu = submenu.menu()
                for sub in submenu:
                    folder = getattr(self.context, m['id'], None)
                    if folder:
                        defaultPage = folder.getDefaultPage()
                        if defaultPage:
                            sub['url'] = '%s/%s' % (sub['url'], defaultPage)
                    sub['id'] = sub['tabId']
                defaultPage = folder.getDefaultPage()
                if defaultPage:
                    m['url'] = '%s/%s' % (m['url'], defaultPage)
                    m['id'] = defaultPage
            if submenu:
                tabListId = 'submenu-%s' % m['id']
                tabPanelsId = 'subpanels-%s' % m['id']
                tabVarId = (defaultPage or m['tabId']).replace('-','_')
                submenuJS += template( tabs = submenu, tabListId = tabListId,
                    tabPanelsId = tabPanelsId, tabVarId = 'tabs%s' % tabVarId )
            m['id'] = m['tabId']

        tabListId = 'webapp-globalnav'
        tabPanelsId = 'content'
        self.request.RESPONSE.setHeader('Content-Type',
                'application/x-javascript')
        self._setCacheHeaders()
        return  self.request.RESPONSE.write( template_main( tabs = menu,
            tabListId = tabListId, tabPanelsId = tabPanelsId,
                        tabVarId = 'tabs', submenu=submenuJS) )


    def subjavascript(self):
        """ Javascript for submenus. """
        context = aq_inner(self.context)
        template = self.template.__of__(context)
        menu = self.menu()
        for m in menu:
            folder = getattr(self.context, m['id'], None)
            if folder:
                submenu = SubMenu(folder, self.request)
                submenu = submenu.menu()
                for sub in submenu:
                    folder = getattr(self.context, m['id'], None)
                    if folder:
                        defaultPage = folder.getDefaultPage()
                        if defaultPage:
                            sub['url'] = '%s/%s' % (sub['url'], defaultPage)
                    sub['id'] = sub['tabId']

            if submenu:
                tabListId = 'submenu-%s' % m['id']
                tabPanelsId = 'subpanels-%s' % m['id']
                return template( tabs = submenu, tabListId = tabListId,
                        tabPanelsId = tabPanelsId, tabVarId = 'tabs%s' %
                                                                m['tabId'])
        return ''

    def inApplication(self):
        """ Boolean if folder isn't on the root of the plone site. """
        root = self._getRoot()
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        return root != aq_base(portal)

class SubMenu(Main):

    def _getRoot(self):
        """ Returns root of submenu. """
        if not putils.base_hasattr(self, '_root'):
            portal_url = getToolByName(self.context, 'portal_url')
            portal = portal_url.getPortalObject()
            obj = self.context
            while  aq_base(obj) is not aq_base(portal):
                parent = putils.parent(obj)
                if IEEAWebApplication.providedBy(parent):
                    break
                obj = parent
            self._root = [obj]
        return self._root[0]

    def pages(self):
        """ Returns pages of submenu folders. """
        catalog = getToolByName(self.context, 'portal_catalog')
        obj = self._getRoot()
        query = {}
        query['path'] =  {'query' : '/'.join(obj.getPhysicalPath()),
                     'depth' : 1 }
        query['review_state'] = 'published'

        portal_properties = getToolByName(self.context, 'portal_properties')
        navtree_properties = getattr(portal_properties, 'navtree_properties')
        # Apply the desired sort
        sortAttribute = navtree_properties.getProperty('sortAttribute', None)
        if sortAttribute is not None:
            query['sort_on'] = sortAttribute
            sortOrder = navtree_properties.getProperty('sortOrder', None)
            if sortOrder is not None:
                query['sort_order'] = sortOrder

        result = catalog.searchResults(query)
        return result

    def onlyOnePage(self):
        """ Boolean if only one page is present. """
        return len(self.pages()) == 1

    def getDefaultPagePanelId(self):
        """ Returns default panel id. """
        return 'panel_subportaltab_%s' % \
                self.getDefaultPageId().replace('-','_')

    def getDefaultPageId(self):
        """ Retrieves the default page id. """
        root = self._getRoot()
        defaultId = root.getDefaultPage()

        if defaultId is None:
            #if no default page, use first page
            pages = self.pages()
            defaultId = pages[0]['getId']
        return defaultId

    def getDefaultPage(self):
        """ Returns the default page. """
        defaultPage = self.context[ self.getDefaultPageId() ]
        view = zope.component.getMultiAdapter((defaultPage, self.request),
                                                            name='subbody')
        self._setCacheHeaders()
        return view()

class PrepareBody(SubMenu):
    """ PrepareBody class of Submenu """
    def _getFoldersToRoot(self):
	""" Return the root of our application. """
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        obj = self.context
        folders = []
        while not IEEAWebApplication.providedBy(obj) and aq_base(obj) \
                                                is not aq_base(portal):
            folders.append(obj.getId())
            obj = putils.parent(obj)
        folders.reverse()
        return folders

    def _ignoreLink(self, link):
        """ ignore links that start with special flags. """
        ignoreLinks = ['/', 'http', 'javascript:' ]
        for start in ignoreLinks:
            if link.startswith(start):
                return True
        return False

    def fixLinks(self, body):
        """ Fix links from page body. """
        folders = self._getFoldersToRoot()[:-1]
        relUrl = re.compile(r"""href=\s*[\"\'](.*?)[\"\']""", re.S)
        links = relUrl.findall(body)
        relFolder = folders.pop()
        for link in links:
            if self._ignoreLink(link):
                continue
            newlink = link
            if link.startswith('../'):
                newlink = link.replace('../', '')
            else:
                newlink = '%s/%s' % (relFolder, link)
            newlink = 'href="%s' % newlink
            link = 'href="%s' % link
            body = body.replace(link, newlink)
        return body

    def prepareBody(self):
        """ Prepares body of page for view. """
        view = zope.component.getMultiAdapter((self.context, self.request),
                                                    name='subbody_unprepared')
        html = view()
        html = self.fixLinks(html)
        return html.replace('src="../', 'src="')


