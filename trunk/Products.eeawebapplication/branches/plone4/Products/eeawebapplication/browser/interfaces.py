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

from zope.interface import Interface

class IWebAppView(Interface):

    def menu():
        """ Returns info for the main tabs. """

    def submenu():
        """ Returns info for sub menu for the current page. """

    def ajax():
        """ Returns the Javascript to register and preload pages. """


class IAjaxTabs(Interface):
    """ generate javascript for the tabs from the content in a webapp """

    def javascript():
        """ Generate javascript for the ajax tabs. """

