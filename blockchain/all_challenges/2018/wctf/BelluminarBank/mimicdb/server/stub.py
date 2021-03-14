def get_messages_summary():
	m = { 
			"from": "John Smith",
			"receivedon": "Yesterday",
			"text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eleifend...",
			"url":"#" 
		}
	messages = list()
	for i in range(3):
		messages.append(m)
	return messages
	
def get_tasks():
	t1 = { "name": "Task 1", "completed" : 40, "type": "success" }
	t2 = { "name": "Task 2", "completed" : 20, "type": "info" }
	t3 = { "name": "Task 3", "completed" : 60, "type": "warning" }
	t4 = { "name": "Task 4", "completed" : 80, "type": "danger" }
	
	return [t1, t2, t3, t4]
	
def get_alerts():
	
	a1 = { "title": "New Comment", "time" : 4, "type": "comment", "url": "#" }
	a2 = { "title": "3 New Followers", "time" : 12, "type": "twitter", "url": "#" }
	a3 = { "title": "Message Sent", "time" : 4, "type": "envelope", "url": "#" }
	a4 = { "title": "New Task", "time" : 4, "type": "tasks", "url": "#" }
	a5 = { "title": "Server Rebooted", "time" : 4, "type": "upload", "url": "#" }
	
	return [a1, a2, a3, a4, a5]
	
def get_adv_tables():
	columns = ["Rendering engine", "Browser", "Platform(s)", "Engine version", "CSS grade"]
	rows = [
		["Trident", "Internet Explorer 4.0", "Win 95+", "4", "X"],
		["Trident", "Internet Explorer 5.0", "Win 95+", "5", "C"],
		["Trident", "Internet Explorer 5.5", "Win 95+", "5.5", "A"],
		["Trident", "Internet Explorer 6", "Win 98+", "6", "A"],
		["Trident", "Internet Explorer 7", "Win XP SP2+", "7", "A"],
		["Trident", "AOL browser (AOL desktop)", "Win XP", "6", "A"],
		["Gecko", "Firefox 1.0", "Win 98+ / OSX.2+", "1.7", "A"],
		["Gecko", "Firefox 1.5", "Win 98+ / OSX.2+", "1.8", "A"],
		["Gecko", "Firefox 2.0", "Win 98+ / OSX.2+", "1.8", "A"],
		["Gecko", "Firefox 3.0", "Win 2k+ / OSX.3+", "1.9", "A"],
		["Gecko", "Camino 1.0", "OSX.2+", "1.8", "A"],
		["Gecko", "Camino 1.5", "OSX.3+", "1.8", "A"],
		["Gecko", "Netscape 7.2", "Win 95+ / Mac OS 8.6-9.2", "1.7", "A"],
		["Gecko", "Netscape Browser 8", "Win 98SE+", "1.7", "A"],
		["Gecko", "Netscape Navigator 9", "Win 98+ / OSX.2+", "1.8", "A"],
		["Gecko", "Mozilla 1.0", "Win 95+ / OSX.1+", "1", "A"],
		["Gecko", "Mozilla 1.1", "Win 95+ / OSX.1+", "1.1", "A"],
		["Gecko", "Mozilla 1.2", "Win 95+ / OSX.1+", "1.2", "A"],
		["Gecko", "Mozilla 1.3", "Win 95+ / OSX.1+", "1.3", "A"],
		["Gecko", "Mozilla 1.4", "Win 95+ / OSX.1+", "1.4", "A"],
		["Gecko", "Mozilla 1.5", "Win 95+ / OSX.1+", "1.5", "A"],
		["Gecko", "Mozilla 1.6", "Win 95+ / OSX.1+", "1.6", "A"],
		["Gecko", "Mozilla 1.7", "Win 98+ / OSX.1+", "1.7", "A"],
		["Gecko", "Mozilla 1.8", "Win 98+ / OSX.1+", "1.8", "A"],
		["Gecko", "Seamonkey 1.1", "Win 98+ / OSX.2+", "1.8", "A"],
		["Gecko", "Epiphany 2.20", "Gnome", "1.8", "A"],
		["Webkit", "Safari 1.2", "OSX.3", "125.5", "A"],
 		["Webkit", "Safari 1.3", "OSX.3", "312.8", "A"],
 		["Webkit", "Safari 2.0", "OSX.4+", "419.3", "A"],
 		["Webkit", "Safari 3.0", "OSX.4+", "522.1", "A"],
		["Webkit", "OmniWeb 5.5", "OSX.4+", "420", "A"],
		["Webkit", "iPod Touch / iPhone", "iPod", "420.1", "A"],
		["Webkit", "S60", "S60", "413", "A"],
		["Presto", "Opera 7.0", "Win 95+ / OSX.1+", "-", "A"],
		["Presto", "Opera 7.5", "Win 95+ / OSX.2+", "-", "A"],
		["Presto", "Opera 8.0", "Win 95+ / OSX.2+", "-", "A"],
		["Presto", "Opera 8.5", "Win 95+ / OSX.2+", "-", "A"],
		["Presto", "Opera 9.0", "Win 95+ / OSX.3+", "-", "A"],
		["Presto", "Opera 9.2", "Win 88+ / OSX.3+", "-", "A"],
		["Presto", "Opera 9.5", "Win 88+ / OSX.3+", "-", "A"],
		["Presto", "Opera for Wii", "Wii", "-", "A"],
		["Presto", "Nokia N800", "N800", "-", "A"],
		["Presto", "Nintendo DS browser", "Nintendo DS", "8.5", "C/A"],
		["KHTML", "Konqureror 3.1", "KDE 3.1", "3.1", "C"],
		["KHTML", "Konqureror 3.3", "KDE 3.3", "3.3", "A"],
		["KHTML", "Konqureror 3.5", "KDE 3.5", "3.5", "A"],
		["Tasman", "Internet Explorer 4.5", "Mac OS 8-9", "-", "X"],
		["Tasman", "Internet Explorer 5.1", "Mac OS 7.6-9", "1", "C"],
		["Tasman", "Internet Explorer 5.2", "Mac OS 8-X", "1", "C"],
		["Misc", "NetFront 3.1", "Embedded devices", "-", "C"],
		["Misc", "NetFront 3.4", "Embedded devices", "-", "A"],
		["Misc", "Dillo 0.8", "Embedded devices", "-", "X"],
		["Misc", "Links", "Text only", "-", "X"],
		["Misc", "Lynx", "Text only", "-", "X"],
		["Misc", "IE Mobile", "Windows Mobile 6", "-", "C"],
		["Misc", "PSP browser", "PSP", "-", "C"],
		["Other browsers","All others","-","-","U"]
	]
	
	return (columns, rows)
	
def get_tables():
	columns = ["#", "First Name", "Last Name", "Username"]
	rows = [
		["1", "Mark", "Otto", "@motto"],
		["2", "Kaushik", "Raj", "@kaushikraj"],
		["3", "Jacob", "Smith", "@jsmith"],
		["4", "Bill", "Clinton", "@thestud"]
	]
	context = [
		"success",
		"info",
		"warning",
		"danger"
	]
	
	return (columns, rows, context)

def get_accordion_items():
	t = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
	items = [
		{ "header" : "Collapsible Group Item #1", "text" : t },
		{ "header" : "Collapsible Group Item #2", "text" : t },
		{ "header" : "Collapsible Group Item #3", "text" : t },
		{ "header" : "Collapsible Group Item #4", "text" : t }
	]
	
	return items
	
def get_tab_items():
	t = "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
	items = [
		{ "tab": "Home", "title" : "Home Tab", "text" : t },
		{ "tab": "Profile", "title" : "Profile Tab", "text" : t },
		{ "tab": "Messages", "title" : "Messages Tab", "text" : t },
		{ "tab": "Settings", "title" : "Settings Tab", "text" : t },
	]
	
	return items