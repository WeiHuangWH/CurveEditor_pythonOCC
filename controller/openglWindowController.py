from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from view.openglWindow import GLWidget
from controller import toolController
from controller.sketchController import SketchController
import logging
from data.sketch.sketch import *
from data.design.part import *

HAVE_PYQT_SIGNAL = hasattr(QtCore, 'pyqtSignal')
from OCC.Core.Geom import Geom_Axis2Placement, Geom_Plane, Geom_Line, Geom_CartesianPoint
from OCC.Core.Prs3d import *
from OCC.Core.Graphic3d import *
from OCC.Core.Quantity import *
from controller.editorController import Sketch_NewSketchEditor
from data.node import *
from OCC.Core.V3d import V3d_Viewer
from OCC.Core.StdSelect import *
from OCC.Core.Graphic3d import *

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


class OpenGLEditor(GLWidget):

    def __init__(self, parent=None):
        super(OpenGLEditor, self).__init__(parent)
        self.InitDriver()
        self.parent = parent
        self._display.set_bg_gradient_color([206, 215, 222], [128, 128, 128])
        self.setDisplayQuality()
        self.setViewCubeController()
        self._display.EnableAntiAliasing()
        # rubberband for selection
        self.myRubberBand = AIS_RubberBand()
        self.myRubberBand.SetFilling(Quantity_Color(Quantity_NOC_GRAY), 0.8)
        self.myRubberBand.SetRectangle(0, 0, 0, 0)
        self._display.Context.Display(self.myRubberBand, True)

        # self._state = self.MODE_VIEW

        self._mousePress_callback = []
        self._mouseMove_callback = []
        self._mouseRelease_callback = []
        self._mouseDoubleClick_callback = []
        self._mouseScroll_callback = []

        self._display.display_triedron()
        # self.setReferenceAxe()
        assert isinstance(self._display.Context, AIS_InteractiveContext)
        # self._display.View.SetBgGradientColors(Quantity_Color(Quantity_NOC_SKYBLUE), Quantity_Color(Quantity_NOC_GRAY), 2, True)
        # selector
        selector_manager: StdSelect_ViewerSelector3d = self._display.Context.MainSelector()
        # self._display.Context.SetPixelTolerance(5)
        selector_manager.SetPixelTolerance(10)
        # camera attribute
        self.view: V3d_View = self._display.View
        # scale factor by mosue scroller
        self.camera: Graphic3d_Camera = self.view.Camera()

    def setDisplayQuality(self):
        ais_context = self._display.GetContext()
        #
        # Display current quality
        dc = ais_context.DeviationCoefficient()
        dc_hlr = ais_context.HLRDeviationCoefficient()
        da = ais_context.DeviationAngle()
        da_hlr = ais_context.HLRAngle()
        print("Default display quality settings:")
        print("Deviation Coefficient: %f" % dc)
        print("Deviation Coefficient Hidden Line Removal: %f" % dc_hlr)
        print("Deviation Angle: %f" % da)
        print("Deviation Angle Hidden Line Removal: %f" % da_hlr)
        #
        # Improve quality by a factor 10
        #
        factor = 1
        ais_context.SetDeviationCoefficient(dc / factor)
        ais_context.SetDeviationAngle(da / factor)
        ais_context.SetHLRDeviationCoefficient(dc_hlr / factor)
        ais_context.SetHLRAngle(da_hlr / factor)
        print("Quality display improved by a factor {0}".format(factor))

    def setViewCubeController(self):
        # view_controller for view manipulation
        self._cubeManip = AIS_ViewCube()
        self._cubeManip.SetTransformPersistence(Graphic3d_TMF_TriedronPers, gp_Pnt(1, 1, 100))
        self._cubeManip.SetInfiniteState(True)
        self._cubeManip.BoxEdgeStyle().SetColor(Quantity_Color(Quantity_NOC_LIGHTGRAY))
        self._cubeManip.BoxCornerStyle().SetColor(Quantity_Color(Quantity_NOC_LIGHTGRAY))
        self._cubeManip.BoxSideStyle().SetColor(Quantity_Color(Quantity_NOC_WHITE))
        self._cubeManip.BoxSideStyle().SetTransparency(0, 1)
        # self._cubeManip.SetDrawVertices(False)
        # self._cubeManip.SetDrawEdges(False)
        # self._cubeManip.SetBoxFacetExtension(0)
        # self._cubeManip.SetInnerColor(Quantity_Color(Quantity_NOC_GRAY))
        self._display.Context.Display(self._cubeManip, True)

    def setReferenceAxe(self):
        geom_axe = Geom_Axis2Placement(gp_XOY())
        self._refrenceAxies = AIS_Trihedron(geom_axe)
        self._refrenceAxies.SetSelectionPriority(Prs3d_DP_XOYAxis, 3)
        self._display.Context.Display(self._refrenceAxies, True)

    def fitSelection(self):
        self._display.Context.FitSelected(self._display.View, 0.0, True)

    def paintEvent(self, event):
        super(OpenGLEditor, self).paintEvent(event)
        if self._inited:
            self._display.Context.UpdateCurrentViewer()
            self.update()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        code = event.key()
        if code in self._key_map:
            functions = self._key_map[code]
            if type(functions) == list:
                for func in functions:
                    func()
            else:
                functions()
        else:
            log.info('key: code %i not mapped to any function' % code)

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
        # print(self.camera.Distance(),self.camera.Scale())
        for callback in self._mouseScroll_callback:
            callback()

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        pt = event.pos()
        buttons = int(event.buttons())
        modifiers = event.modifiers()
        for callback in self._mouseDoubleClick_callback:
            callback()

    def mousePressEvent(self, event):
        self.setFocus()
        pt = event.pos()
        buttons = int(event.buttons())
        modifiers = event.modifiers()
        self.dragStartPosX = pt.x()
        self.dragStartPosY = pt.y()
        if buttons == QtCore.Qt.MiddleButton:
            if modifiers != QtCore.Qt.ShiftModifier:
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
                self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)
            else:
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
        for callback in self._mousePress_callback:
            callback(pt.x(), pt.y(), buttons, modifiers)

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        buttons = int(event.buttons())
        modifiers = event.modifiers()
        for callback in self._mouseRelease_callback:
            callback(buttons, modifiers)
        if event.button() == QtCore.Qt.LeftButton:
            if self._select_area:
                self._display.SelectArea(self.dragStartPosX, self.dragStartPosY, pt.x(), pt.y())
                self._select_area = False
                self.myRubberBand.SetRectangle(0, 0, 0, 0)
                self.myRubberBand.Redisplay(True)
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
        self.myRubberBand.SetRectangle(self.dragStartPosX, self.height() - self.dragStartPosY, pt.x(),
                                       self.height() - pt.y())
        self.myRubberBand.Redisplay(True)

    def mouseMoveEvent(self, evt):
        pt = evt.pos()
        buttons = int(evt.buttons())
        modifiers = evt.modifiers()
        for callback in self._mouseMove_callback:
            callback(pt.x(), pt.y(), buttons, modifiers)

        if buttons == QtCore.Qt.MiddleButton:
            if modifiers != QtCore.Qt.ShiftModifier:
                # ROTATE
                self.cursor = "rotate"
                self._display.Rotation(pt.x(), pt.y())
                self._drawbox = False
            # PAN
            elif modifiers == QtCore.Qt.ShiftModifier:
                dx = pt.x() - self.dragStartPosX
                dy = pt.y() - self.dragStartPosY
                self.dragStartPosX = pt.x()
                self.dragStartPosY = pt.y()
                self.cursor = "pan"
                self._display.Pan(dx, -dy)
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

    def register_mousePress_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mousePress_callback.append(callback)

    def register_mouseMove_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mouseMove_callback.append(callback)

    def register_mouseRelease_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mouseRelease_callback.append(callback)

    def register_mouseDoubleClick_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mouseDoubleClick_callback.append(callback)

    def register_keymap(self, key, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._key_map.setdefault(key, []).append(callback)

    def register_mouseScroll_callback(self, callback):
        if not callable(callback):
            raise AssertionError("You must provide a callable to register the callback")
        else:
            self._mouseScroll_callback.append(callback)


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
