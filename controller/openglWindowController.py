from PyQt5 import QtCore,QtGui,QtWidgets
import sys
from view.openglWindow import GLWidget
from controller import toolController

import logging

HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)
class OpenGLEditor(GLWidget):
    modelUpdated=QtCore.pyqtSignal(object)
    MODE_SKETCH=0
    MODE_DESIGN=1
    MODE_VIEW=2
    def __init__(self, parent=None):
        super(OpenGLEditor, self).__init__(parent)
        self._sceneGraph=None
        self.sketchManager=toolController.SketchController(self._display)
        self._state=self.MODE_VIEW
        #callback functions
        self._display.register_select_callback(self.coordinate_clicked)
        self.sketchManager.modelUpdate.connect(self.addNewItem)
        # from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
        # self.my_box = BRepPrimAPI_MakeBox(1., 2., 3.).Shape()
        # self._display.DisplayShape(self.my_box,update=True)

    def addNewItem(self,item):
        self.modelUpdated.emit(item)
    def setScene(self,scene):
        self._sceneGraph=scene
    def state(self):
        return self._state
    def setState(self,state):
        self._state=state
        print(self._state)
        self.update()
    def processActions(self):
        if self._state==self.MODE_VIEW:
            if self._display.Viewer.IsActive()==True:
                self._display.Viewer.DeactivateGrid()
        elif self._state==self.MODE_DESIGN:
            pass
        elif self._state==self.MODE_SKETCH:
            self.sketchManager.EnterDrawingMode()
        self._display.Repaint()
    def paintEvent(self, event):
        super(OpenGLEditor, self).paintEvent(event)
        self.processActions()
        self.update()

    def coordinate_clicked(self,shp, *kwargs):
        """ This function is called whenever a vertex is selected
        """
        for shape in shp:
            print("Shape selected: ", shape)
        point_2d=kwargs
        x, y, z, vx, vy, vz = self._display.View.ConvertWithProj(kwargs[0],kwargs[1])
    def keyPressEvent(self, event):
        code = event.key()
        if code in self._key_map:
            self._key_map[code]()
        elif code in range(256):
            log.info('key: "%s"(code %i) not mapped to any function' % (chr(code), code))
        else:
            log.info('key: code %i not mapped to any function' % code)
        if code==QtCore.Qt.Key_Escape:
            self.sketchManager.ExitDrawingMode()

    def wheelEvent(self, event):
        try:  # PyQt4/PySide
            delta = event.delta()
        except:  # PyQt5
            delta = event.angleDelta().y()
        if delta > 0:
            zoom_factor = 2.
        else:
            zoom_factor = 0.5
        self._display.ZoomFactor(zoom_factor)
    def mousePressEvent(self, event):
        self.setFocus()
        ev = event.pos()
        self.dragStartPosX = ev.x()
        self.dragStartPosY = ev.y()
        self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)
        x, y, z,vx,vy,vz= self._display.View.ConvertWithProj(ev.x(),ev.y())
        self.sketchManager.setMousePos(x, y, z)

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        modifiers = event.modifiers()

        if event.button() == QtCore.Qt.LeftButton:
            if self._select_area:
                [Xmin, Ymin, dx, dy] = self._drawbox
                self._display.SelectArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                self._select_area = False
            else:
                # multiple select if shift is pressed
                if modifiers == QtCore.Qt.ShiftModifier:
                    self._display.ShiftSelect(pt.x(), pt.y())
                else:
                    # single select otherwise
                    self._display.Select(pt.x(), pt.y())

                    if (self._display.selected_shapes is not None) and HAVE_PYQT_SIGNAL:
                        self.sig_topods_selected.emit(self._display.selected_shapes)


        elif event.button() == QtCore.Qt.RightButton:
            if self._zoom_area:
                [Xmin, Ymin, dx, dy] = self._drawbox
                self._display.ZoomArea(Xmin, Ymin, Xmin + dx, Ymin + dy)
                self._zoom_area = False

        self.cursor = "arrow"

    def DrawBox(self, event):
        tolerance = 2
        pt = event.pos()
        dx = pt.x() - self.dragStartPosX
        dy = pt.y() - self.dragStartPosY
        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            return
        self._drawbox = [self.dragStartPosX, self.dragStartPosY, dx, dy]


    def mouseMoveEvent(self, evt):
        pt = evt.pos()
        buttons = int(evt.buttons())
        modifiers = evt.modifiers()
        # ROTATE
        if (buttons == QtCore.Qt.LeftButton and
                not modifiers == QtCore.Qt.ShiftModifier):
            if modifiers==QtCore.Qt.ControlModifier:
                self.cursor = "rotate"
                self._display.Rotation(pt.x(), pt.y())
                self._drawbox = False
        # DYNAMIC ZOOM
        elif (buttons == QtCore.Qt.RightButton and
              not modifiers == QtCore.Qt.ShiftModifier):
            self.cursor = "zoom"
            self._display.Repaint()
            self._display.DynamicZoom(abs(self.dragStartPosX),
                                      abs(self.dragStartPosY), abs(pt.x()),
                                      abs(pt.y()))
            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self._drawbox = False
        # PAN
        elif buttons == QtCore.Qt.MidButton:
            dx = pt.x() - self.dragStartPosX
            dy = pt.y() - self.dragStartPosY
            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self.cursor = "pan"
            self._display.Pan(dx, -dy)
            self._drawbox = False
        # DRAW BOX
        # ZOOM WINDOW
        elif (buttons == QtCore.Qt.RightButton and
              modifiers == QtCore.Qt.ShiftModifier):
            self._zoom_area = True
            self.cursor = "zoom-area"
            self.DrawBox(evt)
            self.update()
        # SELECT AREA
        elif (buttons == QtCore.Qt.LeftButton and
              modifiers == QtCore.Qt.ShiftModifier):
            self._select_area = True
            self.DrawBox(evt)
            self.update()
        else:
            self._drawbox = False
            self._display.MoveTo(pt.x(), pt.y())
            self.cursor = "arrow"
# -----------------------------Debugging-----------------------------------#
if __name__ == '__main__':
    sys._excepthook = sys.excepthook
    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        print(exctype, value, traceback)
        # Call the normal Exception hook after
        sys._excepthook(exctype, value, traceback)
        sys.exit(1)
    sys.excepthook = my_exception_hook
    application = QtWidgets.QApplication([])
    window = OpenGLEditor()  # Opengl window creation
    window.show()
    application.exec_()
