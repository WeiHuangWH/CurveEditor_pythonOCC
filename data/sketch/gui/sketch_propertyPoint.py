from data.sketch.gui.sketch_property import *
from OCC.Core.Geom2d import Geom2d_CartesianPoint
from OCC.Core.Geom import Geom_CartesianPoint
from OCC.Core.ElCLib import *


class Sketch_PropertyPoint(Sketch_Property):
    def __init__(self, parent, name, fl):
        super(Sketch_PropertyPoint, self).__init__(parent, name, fl)
        if not name:
            self.setObjectName("Property Points")
        self.setFixedSize(300, 300)
        self.ui.TextLabelPoint1.setText("Point. ")
        self.isPointWindow = True
        # UI
        self.ui.TextLabelStyle.close()
        self.ui.ComboBoxStyle.close()
        self.ui.verticalLayout_3.removeWidget(self.ui.GroupBoxPlot)
        self.ui.GroupBoxPlot.close()

    def SetGeometry(self, *__args):
        self.curGeom2d_Point: Geom2d_CartesianPoint =  self.mySObject.GetGeometry2d()
        self.firstPnt2d = self.curGeom2d_Point.Pnt2d()
        self.SetCoord(self.ui.LineEditPoint1, self.firstPnt2d)

    def CheckGeometry(self):
        return self.CheckCoord(self.ui.LineEditPoint1, self.tempPnt2d)

    def GetGeometry(self):
        if not self.firstPnt2d.IsEqual(self.tempPnt2d, 1.0e-6):
            self.firstPnt2d = self.tempPnt2d
            self.curGeom2d_Point.SetPnt2d(self.firstPnt2d)
            self.mySObject.DragTo(self.tempPnt2d)
            return True
        return False
