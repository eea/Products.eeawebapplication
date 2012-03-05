/*
 Ajax Tabs v1.0
 Copyright 2006 HavocStudios.com
	
 Permission is hereby granted, free of charge, to any person obtaining
 a copy of this software and associated documentation files (the
 "Software"), to deal in the Software without restriction, including
 without limitation the rights to use, copy, modify, merge, publish,
 distribute, sublicense, and/or sell copies of the Software, and to
 permit persons to whom the Software is furnished to do so, subject to
 the following conditions:
 
 The above copyright notice and this permission notice shall be
 included in all copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
 LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
 OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
 WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


var AjaxTabs = {
    onClick : function(event) {
                tabListId = this.getAttribute('tabListId');
                tabPanelsId = this.getAttribute('tabPanelsId');
                tmpTabs = new AjaxTabs.Tabs(tabListId, tabPanelsId)
                tmpTabs.FocusTab(this.id);
		return false;
        }

};

AjaxTabs.Tabs = Class.create();
Object.extend(AjaxTabs.Tabs.prototype, {		
 
  initialize : function(tabListId, tabPanelsId) {
     this.tabListId = tabListId;
     this.tabPanelsId = tabPanelsId;

  },

  CloseTab: function(tabId)
		{
			var lastTabId = "";
			var somethingHasFocus = false;
			
			var closeTab = true;
			var closeJS = "if (window.tabClose"+tabId+") { closeTab = tabClose"+tabId+"(); }";
			eval(closeJS);
			if (!closeTab) // user cancelled close tab
			{
				return;
			}

			/* Remove all the event functions for this tab */
			eval("if (window.tabOpen"+tabId+") { tabOpen"+tabId+" = null; }");
			eval("if (window.tabFocus"+tabId+") { tabFocus"+tabId+" = null; }");
			eval("if (window.tabBlur"+tabId+") { tabBlur"+tabId+" = null; }");
			eval("if (window.tabClose"+tabId+") { tabClose"+tabId+" = null; }");

			/* Remove the tab */
			var tabList = document.getElementById(this.tabListId);
			for (i=0; i < tabList.childNodes.length; i++)
			{
				if (tabList.childNodes[i] && tabList.childNodes[i].tagName == "LI" )
				{
					if (tabList.childNodes[i].getAttribute('id') == tabId)
					{
						tabList.removeChild(tabList.childNodes[i]);
					}
				}
			}

			/* Remove the panel */
			var panelList = document.getElementById(this.tabPanelsId);
			for (i=0; i < panelList.childNodes.length; i++)
			{
				if (panelList.childNodes[i] && panelList.childNodes[i].tagName == "DIV" )
				{
					if (panelList.childNodes[i].getAttribute('id') == "panel_" + tabId)
					{
						panelList.removeChild(panelList.childNodes[i]);
					}
				}
			}
		
			// If we closed the tab that had focus, focus on another tab.
			for (i=0; i < tabList.childNodes.length; i++)
			{
				if (tabList.childNodes[i] && tabList.childNodes[i].tagName == "LI" )
				{
					lastTabId = tabList.childNodes[i].getAttribute('id');
					if (tabList.childNodes[i].getAttribute('tabColor') + "selected" == tabList.childNodes[i].className)
					{
						somethingHasFocus = true;
					}
				}
			}
			
			if (!somethingHasFocus)
			{
				this.FocusTab(lastTabId);
			}
		},
				

	 CreateNewTab:	function(tabId, tabLabel, tabURL, tabIsCloseable, tabColor)
		{
			// create the tab
			var newLabel = document.createElement('span');
			newLabel.setAttribute("id", "tabSpan" + tabId);
			newLabel.className = tabColor;
			newLabel.setAttribute("tabColor", tabColor);
			if (tabIsCloseable)
			{
				newLabel.innerHTML = "<div class=\"tabHandle\">" + tabLabel + "</div> <img src=\"x.png\" border=\"0\"  width=\"14\" height=\"14\" onclick=\"CloseTab('" + tabId + "');return false;\" />";
			}
			else
			{
				newLabel.innerHTML = "<div class=\"tabHandle\">" + tabLabel + "</div> <img src=\"spacer.gif\" border=\"0\" width=\"14\" height=\"14\" />";
			}
			
			var oldTab = document.getElementById(tabId);
			var newTab = oldTab
 			if (oldTab == null) {
			    newTab = document.createElement('li'); 
			    newTab.className = tabColor;
                       }


			newTab.setAttribute("id", tabId);
			newTab.setAttribute("tabId", tabId);
			newTab.setAttribute("tabLabel", tabLabel);
			newTab.setAttribute("tabColor", tabColor);
			newTab.setAttribute("tabListId", this.tabListId);
			newTab.setAttribute("tabPanelsId", this.tabPanelsId);
                        newTab.onclick  = AjaxTabs.onClick.bindAsEventListener(newTab);
//                        newTab.onclick = function () { AjaxTabs.onClick(); return false; }
			newTab.setAttribute("tabIsCloseable", "0");
			
			if (tabIsCloseable)
			{
				newTab.setAttribute("tabIsCloseable", "1");
			}
			newTab.setAttribute('isFocused','true');
//			newTab.appendChild(newLabel);
			if (oldTab == null) {
 			     document.getElementById(this.tabListId).appendChild(newTab);
                        }
			
			// create the panel
			var oldPanel = document.getElementById('panel_' + tabId);
			var newPanel = oldPanel
			if (oldPanel == null) {
 			    newPanel = document.createElement('div');
                        }
			newPanel.setAttribute('id','panel_' + tabId);
			newPanel.setAttribute("panelURL", tabURL);
			newPanel.setAttribute("tabColor", tabColor);
			newPanel.className = tabColor + "Panel";
			
			/* newPanel.style.display = "none"; */
                        if (oldPanel == null) {
			document.getElementById(this.tabPanelsId).appendChild(newPanel); }



                         if ( oldTab != null && oldTab.className != 'selected') {
  			  this.RefreshTab(tabId); // load the page up
			} else { 				
    		         eval("if (window.tabFocus"+tabId+") { tabFocus"+tabId+"(); }");
                       }
		},
		
	 GetFocusedTabId: function()
		{
			var tabList = document.getElementById(this.tabListId);
			for (i=0; i < tabList.childNodes.length; i++)
			{
				if (tabList.childNodes[i] && tabList.childNodes[i].tagName == "LI" )
				{
					if (tabList.childNodes[i].className  ==  "selected")
					{
						return tabList.childNodes[i].getAttribute('id');
					}
				}
			}
		},

	FocusTab: function(tabId)
		{

			var currentFocusedTabId = this.GetFocusedTabId();
			
			var tabList = document.getElementById(this.tabListId);
			for (j=0; j < tabList.childNodes.length; j++)
			{
				if (tabList.childNodes[j] && tabList.childNodes[j].tagName == "LI" )
				{
					var className = tabList.childNodes[j].getAttribute("tabColor");
  					if (className == null)
                                        {  className = ''; }
					var currentTabId = tabList.childNodes[j].getAttribute("id");
					if (currentTabId == tabId)
					{
						tabList.childNodes[j].className = className + "selected";
                                                panel = document.getElementById("panel_" + currentTabId)
						panel.className = "selected";
	                       
					}
					else
					{
						tabList.childNodes[j].className = className;

						if(currentTabId != null) {
                                	           panel =  document.getElementById("panel_" + currentTabId)
						   if(panel != null) { 
   						   document.getElementById("panel_" + currentTabId).className = "hidden" ; 
						   }

                                           }

					}
				}
			}
			
			if (tabId != currentFocusedTabId)
			{
				eval("if (window.tabBlur"+currentFocusedTabId+") { tabBlur"+currentFocusedTabId+"(); }");
				eval("if (window.tabFocus"+tabId+") { tabFocus"+tabId+"(); }");
			}
			resizeDiv();
		},
		
	 RefreshTab: function(tabId)
		{
			/* document.getElementById("panel_" + tabId).innerHTML = "Hello, World.<br/>" + document.getElementById("panel_" + tabId).getAttribute("panelURL"); */
			
			var http = getHTTPObject();
			var panel = document.getElementById('panel_' + tabId);
			var page = panel.getAttribute('panelURL');
			var url = page;
			var now = new Date();
			var openFuncExists = false;
			var timeoutId;
			
			// hack to get IE to refresh all the time by making each url unique by adding a timestamp onto it. (ie tries to cache everything)
/*			if (url.indexOf("?") > -1) // this url has get params somewhere
			{
				if (url.substr(url.length-1) == "&") // has a & at the end, no need to append another
				{
					url = url + "t=" + now.getTime();

				}
				else // no & on the end, append it
				{
					url = url + "&t=" + now.getTime();
				}
			}
			else // no params on this url. append a ?
			{
				url = url + "?t=" + now.getTime();
			}
			// end IE hack				
*/
			http.open("GET", url, true);
			http.onreadystatechange = function() {
				if (http.readyState == 4) {
					if (http.status == 200)
					{
						window.clearTimeout(timeoutId);
						var htmlDoc = http.responseText;

						panel = document.getElementById('panel_' + tabId)
          					panel.innerHTML = htmlDoc;
					        scanforlinksinarea(panel);
						if (document.getElementById('script_' + tabId))
						{

							/* Setup the event functions for this tab */
							var script = document.getElementById('script_' + tabId).innerHTML;
							eval(script);
						}
						eval("if (window.tabOpen"+tabId+") { tabOpen"+tabId+"(); }");

					}
				}
			}
			document.getElementById('panel_' + tabId).innerHTML = "<div class='loadingBox'><b>Please wait. Loading...</b> <img src='indicator.gif' /></div>";
			
			http.setRequestHeader("Content-Type","application/x-www-form-urlencoded; charset=UTF-8");
			http.send(null);
			
			timeoutId = window.setTimeout(
				function() {
					switch (http.readyState) {
						case 1:
						case 2:
						case 3:
							http.abort();
							document.getElementById('panel_' + tabId).innerHTML = "<h2>Error Loading Data</h2><a href=\"javascript:void(0)\" onclick=\"this.RefreshTab('" + tabId + "');\">Retry</a>";
							alert("Oops. There was an error retreiving data from the server. Please try again in a few moments.");
							break;
						default:
							break;
					}
				},
				20000 // twenty seconds
			);

   	 },
		
	 TabExists: function(tabId)
		{
			var exists = false;
			var tabList = document.getElementById(this.tabListId);
			for (j=0; j < tabList.childNodes.length; j++)
			{
				if (tabList.childNodes[j] && tabList.childNodes[j].tagName == "LI" )
				{
					var currentTabId = tabList.childNodes[j].getAttribute("tabId");
					var currentTabHTMLId = tabList.childNodes[j].getAttribute("id");
					if (currentTabId == tabId)
					{
						exists = true;
					}
 					if (currentTabHTMLId == tabId)
					{
                     			        tabList.childNodes[j].setAttribute("tabId", tabId);
					}
				}
			}
			return exists;
		},
		
	 OpenTab: function(tabId, tabLabel, tabURL, tabIsCloseable, tabColor)
		{
			if (this.TabExists(tabId))
			{
				this.FocusTab(tabId);
			}
			else
			{
				this.CreateNewTab(tabId, tabLabel, tabURL, tabIsCloseable, tabColor);
			}
	              return false;
		},
		
	 SetTabURL: function(tabId, url)
		{
			document.getElementById('panel_' + tabId).setAttribute('panelURL', url);
			this.RefreshTab(tabId);
		}
});

