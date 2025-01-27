from OCC.Core.Geom import *
from OCC.Core.gp import *
from OCC.Core.AIS import *
from OCC.Core.Aspect import *
from OCC.Core.Prs3d import *
from OCC.Core.Quantity import *
from OCC.Core.Geom2d import *
from OCC.Core.TCollection import *
from OCC.Core.GeomConvert import *
from PyQt5.QtCore import Qt,QModelIndex
from OCC.Core.Geom2dAPI import *
from OCC.Core.GeomAPI import *

from data.model import SceneGraphModel
from data.node import *
from data.sketch.sketch_utils import *
from data.sketch.snaps.sketch_analyserSnap import Sketch_AnalyserSnap
from data.sketch.sketch_type import *
from data.sketch.sketch_object import Sketch_Object

SKETCH_RADIUS = 10.0


class Sketch_Command(object):
    def __init__(self, name):

        self.data = []
        self.rootNode: Node = None
        self.myModel: SceneGraphModel = None
        self.objectName = name
        self.objectCounter = 0
        self.curCoordinateSystem = gp_Ax3(gp.XOY())

        self.myType = Sketch_ObjectType.MainSketchType
        self.myColor = Quantity_Color(Quantity_NOC_YELLOW)
        self.myStyle = Aspect_TOL_SOLID
        self.myWidth = 1.0
        self.myPrs3dAspect = Prs3d_LineAspect(self.myColor, self.myStyle, self.myWidth)

        self.myPolylineMode = False
        self.curPnt2d = gp.Origin2d()
        self.myFirstgp_Pnt2d = gp.Origin2d()
        self.mySecondgp_Pn2d = gp.Origin2d()

        self.myFirstPoint: Geom_CartesianPoint = Geom_CartesianPoint(gp.Origin())
        self.mySecondPoint: Geom_CartesianPoint = Geom_CartesianPoint(gp.Origin())
        # self.myRubberLine = AIS_Line(self.myFirstPoint, self.mySecondPoint)
        # self.myRubberLine.SetColor(Quantity_Color(Quantity_NOC_BLUE1))

    def SetContext(self, theContext: AIS_InteractiveContext):
        self.myContext = theContext

    def SetData(self, theData: list):
        self.data = theData

    def SetRootNode(self, theNode: Node):
        self.rootNode: Node = theNode

    def SetModel(self, theModel):
        self.myModel = theModel

    def SetAx3(self, theAx3: gp_Ax3):
        self.curCoordinateSystem = theAx3

    def SetAnalyserSnap(self, theAnalyserSnap):
        self.myAnalyserSnap: Sketch_AnalyserSnap = theAnalyserSnap

    def SetColor(self, theColor):
        self.myColor = theColor

    def SetType(self, theType):
        self.objectType = theType

    def SetWidth(self, theWidth):
        self.myWidth = theWidth

    def SetStyle(self, theLineStyle):
        self.myStyle = theLineStyle

    def AddObject(self, theGeom2d_Geometry: Geom2d_Geometry, theAIS_InteractiveObject: AIS_InteractiveObject,
                  theGeometryType: Sketch_GeometryType):
        self.objectCounter += 1
        numString = str(self.objectCounter)
        currentName = self.objectName
        currentName += numString
        if self.GetTypeOfMethod() == Sketch_ObjectTypeOfMethod.Point_Method:
            theAIS_InteractiveObject.SetColor(self.myColor)
        else:
            self.myPrs3dAspect.SetColor(self.myColor)
            self.myPrs3dAspect.SetTypeOfLine(self.myStyle)
            self.myPrs3dAspect.SetWidth(self.myWidth)

        so = Sketch_Object(theGeom2d_Geometry, theAIS_InteractiveObject, currentName, theGeometryType,
                           self.GetTypeOfMethod())
        so.SetColor(self.myColor)
        so.SetType(self.myType)
        so.SetStyle(self.myStyle)
        so.SetWidth(self.myWidth)
        self.myModel.layoutChanged.emit()
        self.data.append(so)

    def GetTypeOfMethod(self):
        raise NotImplementedError()

    def Action(self):
        raise NotImplementedError()

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        raise NotImplementedError()

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        raise NotImplementedError()

    def MouseReleaseEvent(self, buttons, modifiers):
        pass

    def CancelEvent(self):
        raise NotImplementedError()

    def SetPolylineFirstPnt(self, p1):
        pass

    def GetPolylineFirstPnt(self, p1):
        pass

    def SetPolylineMode(self, mode):
        pass
