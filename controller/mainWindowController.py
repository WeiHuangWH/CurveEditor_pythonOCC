from view import mainWindow
from controller import editorController, openglWindowController, sketchController, partController, viewController,menuController
import resources.icon.icon
from data.model import *


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self._ui = mainWindow.Ui_MainWindow()
        self._ui.setupUi(self)

        # setup data
        self._rootNode = Node("Scene")
        self._model = SceneGraphModel(self._rootNode)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # """VIEW <------> PROXY MODEL <------> DATA MODEL"""
        # self._proxyModel = QtCore.QSortFilterProxyModel()
        # self._proxyModel.setSourceModel(self._model)

        # self._proxyModel.setDynamicSortFilter(True)
        # self._proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        #
        # self._proxyModel.setSortRole(SceneGraphModel.sortRole)
        # self._proxyModel.setFilterRole(SceneGraphModel.filterRole)

        # opengl window
        self._glWindow = openglWindowController.OpenGLEditor(self)
        self.setCentralWidget(self._glWindow)

        # setup sceneGraph editor
        self._uiTreeView = viewController.CustomTreeViewController()
        self._uiTreeView.setModel(self._model)
        # view manager
        self.viewController = viewController.ViewController( self)
        # sketch manager
        self.sketchController = sketchController.SketchController(self)
        self.sketchController.setModel(self._model)
        self.sketchController.setRootNode(self._rootNode)
        self._glWindow.register_mousePress_callback(self.sketchController.OnMouseInputEvent)
        self._glWindow.register_mouseMove_callback(self.sketchController.OnMouseMoveEvent)
        self._glWindow.register_mouseRelease_callback(self.sketchController.OnMouseReleaseEvent)
        self._glWindow.register_mouseDoubleClick_callback(self.sketchController.editGeometry)
        self._glWindow.register_keymap(QtCore.Qt.Key_Escape, self.sketchController.OnCancel)
        self._glWindow.register_keymap(QtCore.Qt.Key_Delete, self.sketchController.DeleteSelectedObject)
        # part manager
        self.partController = partController.PartController(self)
        self.partController.setModel(self._model)
        self.partController.setRootNode(self._rootNode)
        self._glWindow.register_mousePress_callback(self.partController.OnMouseInputEvent)
        self._glWindow.register_mouseMove_callback(self.partController.OnMouseMoveEvent)
        self._glWindow.register_keymap(QtCore.Qt.Key_Escape, self.partController.OnCancel)
        self._glWindow.register_keymap(QtCore.Qt.Key_Delete, self.partController.DeleteSelectedObject)
        #menu manager
        self.menuBarController=menuController.MenuBarController(self)
        # setup tool bar
        self.createToolBars()

        # create sceneGraph dock widget
        self._sceneGraphDock = QtWidgets.QDockWidget("Scene", self)
        self._sceneGraphDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self._sceneGraphDock.setWidget(self._uiTreeView)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._sceneGraphDock)

        # setup property editor
        self._propEditor = editorController.PropertyEditor(self)
        self._propEditor.setModel(self._model)

        # create property dock widget
        self._propertyDock = QtWidgets.QDockWidget("Scene", self)
        self._propertyDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self._propertyDock.setWidget(self._propEditor)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self._propertyDock)

        # create tool dock widget
        # self._toolBarDock = QtWidgets.QDockWidget("Tool", self)
        # self._toolBarDock.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)

        # set two vertical toolbar in the tool widget
        self._toolBarLayout = QtWidgets.QVBoxLayout()

        self._toolBarLayout.setMenuBar(self._curveToolBar)
        # self._toolBarLayout.setMenuBar(self._surfaceToolBar)

        self._toolBarContainer = QtWidgets.QWidget()
        self._toolBarContainer.setLayout(self._toolBarLayout)

        # self._toolBarDock.setWidget(self._toolBarContainer)
        # self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self._toolBarDock)

        # sceneGraph and property synchronization
        self._uiTreeView.selectionModel().currentChanged.connect(self._propEditor.setSelection)
        self._uiTreeView.selectionModel().currentChanged.connect(self.sketchController.highlightCurrentNode)
        self._uiTreeView.model().rowsRemoved.connect(self.checkCurrentPlane)
        self.sketchController.sketchPlaneUpdated.connect(self.selectPlane)

    def checkCurrentPlane(self, parent: QtCore.QModelIndex, first, last):
        print(self._model.getNode(parent), self.sketchController.currentSketchNode, first, last)
        print(self._model.rowCount(parent))
        if self._model.rowCount(parent)==0:
            # self.sketchController.currentSketchNode = None
            pass
    def selectPlane(self, item):
        '''

        Args:
            item: Mesh node (usually represent shape node)

        Returns:

        '''
        position = self._rootNode.childCount()
        self._propEditor.setModel(self._model)
        # select latest row
        self._uiTreeView.setCurrentIndex(self._model.index(position, 0, QtCore.QModelIndex()))
        self._uiTreeView.updateEditorData()
        self._uiTreeView.expandAll()

    def selectSketchObjects(self, position, parent):
        self._uiTreeView.setCurrentIndex(self._model.index(position - 1, 0, parent))
        self._uiTreeView.updateEditorData()
        self._uiTreeView.expandAll()

    def createToolBars(self):
        # Curve tool bar
        self._curveToolBar = QtWidgets.QToolBar("Curve")
        self._curveToolBar.setOrientation(QtCore.Qt.Vertical)
        # Surface tool bar
        self._surfaceToolBar = QtWidgets.QToolBar("Surface")
        self._surfaceToolBar.setOrientation(QtCore.Qt.Vertical)
        # View tool bar
        self._viewToolBar = QtWidgets.QToolBar("View")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._viewToolBar)
        self._viewToolBar.setOrientation(QtCore.Qt.Horizontal)
        for action in self.viewController.actions:
            self.createToolButton(action, self._viewToolBar)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._viewToolBar)
        # Toolbar for different modes
        self._sketchToolBar = QtWidgets.QToolBar("Sketch")
        for action in self.sketchController.actions:
            if type(action) == list:
                self.createToolButtonWithMenu(action, self._sketchToolBar)
            else:
                self.createToolButton(action, self._sketchToolBar)
        self._designToolBar = QtWidgets.QToolBar("Design")
        for action in self.partController.actions:
            if type(action) == list:
                self.createToolButtonWithMenu(action, self._designToolBar)
            else:
                self.createToolButton(action, self._designToolBar)
        self.addToolBar(QtCore.Qt.TopToolBarArea, self._designToolBar)

        self._toolTabWidget = QtWidgets.QTabWidget()
        self._toolTabWidget.addTab(self._viewToolBar, "View")
        self._toolTabWidget.addTab(self._sketchToolBar, "Sketch")
        self._toolTabWidget.addTab(self._designToolBar, "Design")
        self._ui.toolBar.addWidget(self._toolTabWidget)
        # set dockwidget as menubar
        # self.setMenuWidget(self._toolTabWidget)

    def createToolButton(self, action, parent):
        button = QtWidgets.QToolButton(self)
        button.setDefaultAction(action)
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        # button.setStyleSheet("QToolButton {color: #333; border: 2px solid #555; border-radius: 11px; padding: 5px; background: qradialgradient(cx: 0.3, cy: -0.4,fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #888); min-width: 80px;}"
        #     "QToolButton:hover {background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #bbb);}"
        #     "QToolButton:pressed { background: qradialgradient(cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1, radius: 1.35, stop: 0 #fff, stop: 1 #ddd);}")
        button.setMinimumSize(100, 50)
        button.setIconSize(QtCore.QSize(50, 30))
        button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        button.setAutoRaise(True)
        parent.addWidget(button)

    def createToolButtonWithMenu(self, actions, parent):
        button = QtWidgets.QToolButton(self)
        menu = QtWidgets.QMenu()
        for action in actions:
            menu.addAction(action)

        button.setMenu(menu)
        button.setDefaultAction(actions[0])
        button.setPopupMode(QtWidgets.QToolButton.MenuButtonPopup)
        button.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        button.triggered.connect(button.setDefaultAction)
        # button.setStyleSheet("QToolButton {color: #333; border: 2px solid #555; border-radius: 11px; padding: 5px; background: qradialgradient(cx: 0.3, cy: -0.4,fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #888); min-width: 80px;}"
        #     "QToolButton:hover {background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 1.35, stop: 0 #fff, stop: 1 #bbb);}"
        #     "QToolButton:pressed { background: qradialgradient(cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1, radius: 1.35, stop: 0 #fff, stop: 1 #ddd);}")
        button.setMinimumSize(100, 50)
        button.setIconSize(QtCore.QSize(50, 30))
        button.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.MinimumExpanding)
        button.setAutoRaise(True)
        parent.addWidget(button)


