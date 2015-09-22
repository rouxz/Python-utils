import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *






# création de la view and container 
class TopWindow(QMainWindow):
	""" create a window being the main window of the gui """
	def __init__(self, debug=True):
		# initiate the main widget
		QMainWindow.__init__(self)


		self.debug = debug

		# init the window
		self.initTopWindow(self.fm, self.core)

		#connect slots and signals
		self.connect(self, SIGNAL('triggered()'), self.quitApplication)
		self.connect(self, SIGNAL('destroyed()'), self.quitApplication)
		self.connect(self, SIGNAL('quit()'), self.quitApplication)


	""" initiate the top window """
	def initTopWindow(self, fm, core):


		########################
		# Status and menu bars
		########################

		#set the status bar
		self.statusBar().showMessage('Ready')

		# set the menu bar
		self.defineMenu()

		#######################"
		# central widget
		########################

		self.centralWidget = CentralWidget(fm, core, self, self.statusBar(), self.params)
		self.setCentralWidget(self.centralWidget)


		#pack the window
		self.setWindowTitle(TITLE_TOPWINDOW)

		self.show()

	def defineMenu(self):
		""" define menu of the application"""
		# exit button
		exitAction = QAction('&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.setStatusTip('Exit application')
		exitAction.triggered.connect(self.quitApplication)
		# exitAction.triggered.connect(qApp.quit)

		# db switch
		switch_db = QAction('&Switch database', self)
		switch_db.setShortcut('Ctrl+S')
		switch_db.setStatusTip('Change local databse')
		switch_db.triggered.connect(self.switcher_db)
		
		# remote server button
		remoteServer = QAction('&Remote server', self)
		remoteServer.setShortcut('Ctrl+R')
		remoteServer.setStatusTip('Deal with remote server')
		remoteServer.triggered.connect(self.launchRemoteServer)

		#about button
		aboutAction = QAction("&About " + PROG_SHORT_NAME, self)
		aboutAction.setStatusTip('About')
		self.connect(aboutAction, SIGNAL("triggered()"), self.launchAbout)

		# main menu bar
		self.menubar = self.menuBar()
		# fileMenu
		self.fileMenu = self.menubar.addMenu('&File')
		self.fileMenu.addAction(switch_db)
		self.fileMenu.addAction(remoteServer)
		self.fileMenu.addAction(exitAction)

		#help menu
		self.helpMenu = self.menubar.addMenu("&?")
		self.helpMenu.addAction(aboutAction)


	def launchAbout(self):
		pass


	def	quitApplication(self):
		qApp.quit()
			
	def closeEvent(self, e):
		self.quitApplication()

# ###########################################
#
#	Central widget
#
# ############################################


class CentralWidget(QWidget):
	""" a widget being the main widget within the topwindow"""
	""" this main widget will have all the required tabs and table within """
	def __init__(self, fm, core, parent, status, params):
		QWidget.__init__(self, parent)

		
		self.params = params
		# operating system
		# self.platform = platform

		# status bar
		self.status = status

		#init the central widget
		self.initCentralWidget(fm, core, self.params.debug)

	def initCentralWidget(self, fm, core, debug):
		#the top grid layout and tweak it


		self.grid = QGridLayout()
		self.grid.setSpacing(GRID_LAYOUT_SPACE)

		#SIDE PANEL
		self.sidePanel = SidePanel(fm, core, self, self.status, debug)

		#######################"
		# Place all the items
		########################



		# set the tabs
		self.tabsWidget = Tabs(core, self.sidePanel, self.status, self, self.params)
		self.grid.addWidget(self.tabsWidget, 1 , 0, 1, -1)


		# set the title
		self.title = QLabel(self)
		self.title.setText(TITLE_TOPWINDOW)
		self.grid.addWidget(self.title, 0 , 0, 1, -1)

		# set the side panel
		self.grid.addWidget(self.sidePanel, 2, 1)

		#setting the layout

		self.grid.setVerticalSpacing(1)
		self.setLayout(self.grid)
