from data.sketch.commands.sketch_command import *
from OCC.Core.ElCLib import elclib
from enum import Enum

from OCC.Core.GC import *
from OCC.Core.gce import *

M_PI = 3.14159


class ArcCenter2PAction(Enum):
    Nothing = 0
    Input_CenterArc = 1
    Input_1ArcPoint = 2
    Input_2ArcPoint = 3


class Sketch_CommandArcCenter2P(Sketch_Command):
    def __init__(self):
        super(Sketch_CommandArcCenter2P, self).__init__("Arc3P.")
        self.myArcCenter2PAction = ArcCenter2PAction.Nothing
        self.radius = 0.0
        self.tempGeom_Circle = Geom_Circle(self.curCoordinateSystem.Ax2(), SKETCH_RADIUS)
        self.myRubberCircle = AIS_Circle(self.tempGeom_Circle)
        self.myRubberCircle.SetColor(Quantity_Color(Quantity_NOC_BLUE1))
        self.myCircleAx2d = gp_Ax2d()
        self.ProjectOnCurve = Geom2dAPI_ProjectPointOnCurve()
        coordinate = "Degree: {}".format(0)
        self.myAIS_Label = self.CreateLabel(coordinate, Quantity_NOC_GREEN, offset=gp_Vec(0, 0, 0))

    def Action(self):
        self.myArcCenter2PAction = ArcCenter2PAction.Input_CenterArc

    def MouseInputEvent(self, thePnt2d: gp_Pnt2d, buttons, modifier):
        if self.myArcCenter2PAction == ArcCenter2PAction.Nothing:
            pass
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_CenterArc:
            self.tempGeom_Circle = Geom_Circle(self.curCoordinateSystem.Ax2(), SKETCH_RADIUS)

            self.curPnt2d = self.myAnalyserSnap.MouseInput(thePnt2d)
            self.myFirstgp_Pnt2d = gp_Pnt2d(self.curPnt2d.X(), self.curPnt2d.Y())
            self.myFirstPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.myFirstgp_Pnt2d))

            self.myCircleAx2d.SetLocation(self.myFirstgp_Pnt2d)
            self.tempGeom_Circle.SetLocation(self.myFirstPoint.Pnt())
            self.tempGeom_Circle.SetRadius(SKETCH_RADIUS)

            self.myRubberCircle.SetCircle(self.tempGeom_Circle)
            self.myRubberCircle.SetFirstParam(0)
            self.myRubberCircle.SetLastParam(M_PI * 2)
            self.myContext.Display(self.myRubberCircle, True)
            self.myArcCenter2PAction = ArcCenter2PAction.Input_1ArcPoint

        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_1ArcPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseInputException(self.myFirstgp_Pnt2d, thePnt2d,
                                                                    TangentType.Circle_CenterPnt, True)
            self.radius = self.myFirstgp_Pnt2d.Distance(self.curPnt2d)
            self.tempGeom_Circle.SetRadius(self.radius)
            self.myRubberCircle.SetCircle(self.tempGeom_Circle)
            self.tempGeom2d_Circle = Geom2d_Circle.DownCast(
                geomapi_To2d(self.tempGeom_Circle, gp_Pln(self.curCoordinateSystem)))

            self.myContext.Redisplay(self.myRubberCircle, True)
            # update text
            self.myAIS_Label.SetPosition(self.tempGeom_Circle.Location())
            self.myContext.Display(self.myAIS_Label, True)
            self.myArcCenter2PAction = ArcCenter2PAction.Input_2ArcPoint
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_2ArcPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
            if self.ProjectOnCircle(self.curPnt2d):
                third_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
                self.myRubberCircle.SetCircle(self.tempGeom_Circle)
                p1 = elclib.Parameter(self.tempGeom_Circle.Circ(), self.mySecondPoint.Pnt())
                p2 = elclib.Parameter(self.tempGeom_Circle.Circ(), third_Pnt)
                self.myRubberCircle.SetFirstParam(min(p1, p2))
                self.myRubberCircle.SetLastParam(max(p1, p2))

                self.myGeomArc = Geom2d_Arc(self.tempGeom2d_Circle.Circ2d())
                self.myGeomArc.SetFirstParam(min(p1, p2))
                self.myGeomArc.SetLastParam(max(p1, p2))
                # Remove text
                self.myContext.Remove(self.myAIS_Label, True)
                self.myContext.Remove(self.myRubberCircle, True)

                nurbs = self.ArcToNurbsArc(min(p1, p2), max(p1, p2))
                self.bspline_node = BsplineNode(nurbs.GetName(), self.rootNode)
                self.bspline_node.setSketchObject(nurbs)
                self.AddObject(self.myGeomArc, nurbs.GetAIS_Object(), Sketch_GeometryType.ArcSketchObject)

            self.myArcCenter2PAction = ArcCenter2PAction.Nothing
        return False

    def MouseMoveEvent(self, thePnt2d: gp_Pnt2d, buttons, modifiers):
        if self.myArcCenter2PAction == ArcCenter2PAction.Nothing:
            pass
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_CenterArc:
            self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_1ArcPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseMoveException(self.myFirstgp_Pnt2d, thePnt2d,
                                                                   TangentType.Circle_CenterPnt, True)
            self.radius = self.myFirstgp_Pnt2d.Distance(self.curPnt2d)
            if self.radius == 0.0:
                self.radius = 1.0
            self.tempGeom_Circle.SetRadius(self.radius)
            self.myContext.Redisplay(self.myRubberCircle, True)
            self.mySecondPoint.SetPnt(elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d))
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_2ArcPoint:
            self.curPnt2d = self.myAnalyserSnap.MouseMove(thePnt2d)
            if self.ProjectOnCircle(self.curPnt2d):
                third_Pnt = elclib.To3d(self.curCoordinateSystem.Ax2(), self.curPnt2d)
                self.myRubberCircle.SetCircle(self.tempGeom_Circle)
                p1 = elclib.Parameter(self.tempGeom_Circle.Circ(), self.mySecondPoint.Pnt())
                p2 = elclib.Parameter(self.tempGeom_Circle.Circ(), third_Pnt)
                self.myRubberCircle.SetFirstParam(min(p1, p2))
                self.myRubberCircle.SetLastParam(max(p1, p2))
                self.myContext.Redisplay(self.myRubberCircle, True)
                # update text
                degree = "Degree: {}".format(round(p2 * 180 / M_PI))
                self.myAIS_Label.SetText(TCollection_ExtendedString(degree))
                self.myContext.Redisplay(self.myAIS_Label, True)

    def CancelEvent(self):
        if self.myArcCenter2PAction == ArcCenter2PAction.Nothing:
            pass
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_CenterArc:
            pass
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_1ArcPoint:
            self.myContext.Remove(self.myRubberCircle, True)
        elif self.myArcCenter2PAction == ArcCenter2PAction.Input_2ArcPoint:
            self.myContext.Remove(self.myRubberCircle, True)
            self.myContext.Remove(self.myAIS_Label, True)
        self.myArcCenter2PAction = ArcCenter2PAction.Nothing

    def GetTypeOfMethod(self):
        return Sketch_ObjectTypeOfMethod.ArcCenter2P_Method

    def ArcToNurbsArc(self, p1, p2):
        temp_curve = GC_MakeArcOfCircle(self.tempGeom_Circle.Circ(), p1, p2, False)
        if temp_curve.Status() == gce_Done:
            nurbsArc = Sketch_Bspline(self.myContext, self.curCoordinateSystem)

            convert: Geom_BSplineCurve = geomconvert_CurveToBSplineCurve(temp_curve.Value())
            poles = TColgp_Array1OfPnt2d_to_point_list(convert.Poles())
            weights = TColStd_Array1OfNumber_to_list(convert.Weights())
            knots = TColStd_Array1OfNumber_to_list(convert.Knots())
            multiplicity = TColStd_Array1OfNumber_to_list(convert.Multiplicities())

            for pole in poles:
                x, y = pole.X(), pole.Y()
                nurbsArc.AddPoles(gp_Pnt2d(x, y))
            nurbsArc.SetWeights(weights)
            nurbsArc.SetKnots(knots)
            nurbsArc.SetMultiplicities(multiplicity)
            nurbsArc.SetDegree(convert.Degree())

            nurbsArc.Compute()
            return nurbsArc

    def ProjectOnCircle(self, thePnt2d):
        self.ProjectOnCurve.Init(thePnt2d, self.tempGeom2d_Circle)
        if self.ProjectOnCurve.NbPoints() > 0:
            self.curPnt2d = self.ProjectOnCurve.NearestPoint()
            return True
        return False

    def CreateLabel(self, text: str, color, offset=gp_Vec(20, 20, 20)):
        # Text label
        myAIS_Text = AIS_TextLabel()
        myAIS_Text.SetText(
            TCollection_ExtendedString(text))
        myAIS_Text.SetPosition(self.tempGeom_Circle.Location().Translated(offset))
        myAIS_Text.SetColor(Quantity_Color(color))
        return myAIS_Text
