class NodeType:
    Node="Node"
    SketchNode="Plane"
    SketchObjectNode="SketchObject"
    PointNode="Point"
    LineNode="Line"
    BezierNode="Bezier Curve"
    BsplineNode="Bspline"

    BsplineSurfaceNode="Bspline Surface"
    BezierSurfaceNode="Bezier Surface"
    RevolvedSurfaceNode="Surface of Revolution"
    ExtrudedSurfaceNode="Ruled Surface"
    SweepSurfaceNode="Sweep Surface"
    ImportedSurfaceNode="Imported Surface"
class Node(object):

    def __init__(self, name, parent=None):
        '''
        Args:
            name: name of the node
            parent: parent pointer
        '''
        super(Node, self).__init__()
        self._name = name
        self._parent = parent
        self._children = []
        if parent is not None:
            parent.addChild(self)

    def typeInfo(self):
        return NodeType.Node

    def addChild(self, child):
        self._children.append(child)
        child._parent = self

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def child(self, row):
        if self._children:
            if row > len(self._children) - 1:
                return None
            else:
                return self._children[row]
        return None

    def children(self):
        return self._children

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False
        self._children.insert(position, child)
        child._parent = self
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False
        child = self._children.pop(position)
        if isinstance(child, SketchNode):
            child.getSketchPlane().RemoveDisplay()
            index = 0
            while index < child.childCount():
                myCurObject = child.child(index).getSketchObject()
                myCurObject.RemoveDisplay()
                index += 1
        elif isinstance(child, SketchObjectNode):
            myCurObject = child.getSketchObject()
            myCurObject.RemoveDisplay()
        child._parent = None
        del child
        return True

    def childCount(self):
        return len(self._children)

    def parent(self):
        return self._parent

    def row(self):
        if self._parent is not None:
            return self._parent._children.index(self)

    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1
        for i in range(tabLevel):
            output += "\t"
        output += "|------" + self._name + "\n"
        for child in self._children:
            output += child.log(tabLevel)
        tabLevel -= 1
        return output

    def __repr__(self):
        return self.log()

    def data(self, column):
        if column == 0:
            return self._name
        elif column == 1:
            return self.typeInfo()

    def setData(self, column, value):
        if column == 0:
            self._name = value
        elif column == 1:
            pass

    def resource(self):
        return None


class SketchNode(Node):
    def __init__(self, name, parent=None):
        super(SketchNode, self).__init__(name, parent)
        self.sketchPlane: Sketch_Plane = None
        self.shapeObject = None
    def setSketchPlane(self, thePlane):
        self.sketchPlane = thePlane

    def getSketchPlane(self):
        return self.sketchPlane

    def typeInfo(self):
        return NodeType.SketchNode


from OCC.Core.gp import *

from data.sketch.geometry import *
from data.sketch.sketch_object import Sketch_Object
from data.design.geometry import *


class SketchObjectNode(Node):
    def __init__(self, name, parent=None):
        super(SketchObjectNode, self).__init__(name, parent)
        self.sketchObject: Sketch_Geometry = None
        self.shapeObject=None
    def setSketchObject(self, theObject: Sketch_Object):
        self.sketchObject = theObject

    def getSketchObject(self):
        return self.sketchObject

    def typeInfo(self):
        return NodeType.SketchObjectNode


class PointNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(PointNode, self).__init__(name, parent)
        self.sketchObject: Sketch_Point = None

    def setData(self, column, value):
        super(SketchObjectNode, self).setData(column, value)
        # show in viewport
        if column == 2:
            self.sketchObject.showViewportObject = value
            self.sketchObject.DisplayObject()
        # shows auxiliry line
        elif column == 3:
            self.sketchObject.showVieportAuxilirayLine = value
            self.sketchObject.DisplayAuxiliryLine()
        # viewport name
        elif column == 4:
            self.sketchObject.showViewportName = value
            self.sketchObject.DisplayName()
        # viewport coordinate
        elif column == 5:
            self.sketchObject.showViewportCoordinate = value
            self.sketchObject.DisplayCoordinate()

    def data(self, column):
        r = super(SketchObjectNode, self).data(column)
        # show in viewport
        if column == 2:
            r = self.sketchObject.myContext.IsDisplayed(self.sketchObject.GetAIS_Object())
        # selectable
        elif column == 3:
            r = self.sketchObject.showVieportAuxilirayLine
        # viewport name
        elif column == 4:
            r = self.sketchObject.showViewportName
        # viewport coordinate
        elif column == 5:
            r = self.sketchObject.showViewportCoordinate
        return r

    def typeInfo(self):
        return NodeType.PointNode

    def resource(self):
        return ":/point.png"


class LineNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(LineNode, self).__init__(name, parent)
        self.sketchObject: Sketch_Line = None

    def setData(self, column, value):
        super(SketchObjectNode, self).setData(column, value)
        # show in viewport
        if column == 2:
            self.sketchObject.showViewportObject = value
            self.sketchObject.DisplayObject()
        # shows auxiliry line
        elif column == 3:
            self.sketchObject.showVieportAuxilirayLine = value
            self.sketchObject.DisplayAuxiliryLine()
        # viewport name
        elif column == 4:
            self.sketchObject.showViewportName = value
            self.sketchObject.DisplayName()
        # viewport coordinate
        elif column == 5:
            self.sketchObject.showViewportCoordinate = value
            self.sketchObject.DisplayCoordinate()

    def data(self, column):
        r = super(SketchObjectNode, self).data(column)
        # show in viewport
        if column == 2:
            r = self.sketchObject.myContext.IsDisplayed(self.sketchObject.GetAIS_Object())
        # selectable
        elif column == 3:
            r = self.sketchObject.showVieportAuxilirayLine
        # viewport name
        elif column == 4:
            r = self.sketchObject.showViewportName
        # viewport coordinate
        elif column == 5:
            r = self.sketchObject.showViewportCoordinate
        return r

    def typeInfo(self):
        return NodeType.LineNode

    def resource(self):
        return ":/inputLine.png"


from OCC.Core.Geom2d import Geom2d_BezierCurve


class BezierNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BezierNode, self).__init__(name, parent)
        self.sketchObject: Sketch_BezierCurve = None

    def setData(self, column, value):
        super(SketchObjectNode, self).setData(column, value)
        # show in viewport
        if column == 2:
            self.sketchObject.showViewportObject = value
            self.sketchObject.DisplayObject()
        # shows auxiliry line
        elif column == 3:
            self.sketchObject.showVieportAuxilirayLine = value
            self.sketchObject.DisplayAuxiliryLine()
        # viewport name
        elif column == 4:
            self.sketchObject.showViewportName = value
            self.sketchObject.DisplayName()
        # viewport coordinate
        elif column == 5:
            self.sketchObject.showViewportCoordinate = value
            self.sketchObject.DisplayCoordinate()

    def data(self, column):
        r = super(SketchObjectNode, self).data(column)
        # show in viewport
        if column == 2:
            r = self.sketchObject.myContext.IsDisplayed(self.sketchObject.GetAIS_Object())
        # selectable
        elif column == 3:
            r = self.sketchObject.showVieportAuxilirayLine
        # viewport name
        elif column == 4:
            r = self.sketchObject.showViewportName
        # viewport coordinate
        elif column == 5:
            r = self.sketchObject.showViewportCoordinate
        return r

    def typeInfo(self):
        return NodeType.BezierNode

    def resource(self):
        return ":/bezier_curve.png"


class BsplineNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BsplineNode, self).__init__(name, parent)

    def setData(self, column, value):
        super(SketchObjectNode, self).setData(column, value)
        # show in viewport
        if column == 2:
            self.sketchObject.showViewportObject = value
            self.sketchObject.DisplayObject()
        # shows auxiliry line
        elif column == 3:
            self.sketchObject.showVieportAuxilirayLine = value
            self.sketchObject.DisplayAuxiliryLine()
        # viewport name
        elif column == 4:
            self.sketchObject.showViewportName = value
            self.sketchObject.DisplayName()
        # viewport coordinate
        elif column == 5:
            self.sketchObject.showViewportCoordinate = value
            self.sketchObject.DisplayCoordinate()

    def data(self, column):
        r = super(SketchObjectNode, self).data(column)
        # show in viewport
        if column == 2:
            r = self.sketchObject.myContext.IsDisplayed(self.sketchObject.GetAIS_Object())
        # selectable
        elif column == 3:
            r = self.sketchObject.showVieportAuxilirayLine
        # viewport name
        elif column == 4:
            r = self.sketchObject.showViewportName
        # viewport coordinate
        elif column == 5:
            r = self.sketchObject.showViewportCoordinate
        return r

    def typeInfo(self):
        return NodeType.BsplineNode

    def resource(self):
        return ":/bspline_curve.png"


class BezierSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BezierSurfaceNode, self).__init__(name, parent)

    def data(self, column):
        r = super(BezierSurfaceNode, self).data(column)

        return r

    def setData(self, column, value):
        super(BezierSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return NodeType.BezierSurfaceNode

    def resource(self):
        return ":/bezier_surface.png"


class BsplineSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(BsplineSurfaceNode, self).__init__(name, parent)

    def data(self, column):
        r = super(BsplineSurfaceNode, self).data(column)

        return r

    def setData(self, column, value):
        super(BsplineSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return NodeType.BsplineSurfaceNode

    def resource(self):
        return ":/bspline_surface.png"


class RevolvedSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(RevolvedSurfaceNode, self).__init__(name, parent)

    def data(self, column):
        r = super(RevolvedSurfaceNode, self).data(column)

        return r

    def setData(self, column, value):
        super(RevolvedSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return NodeType.RevolvedSurfaceNode

    def resource(self):
        return ":/revolve.png"


class ExtrudedSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(ExtrudedSurfaceNode, self).__init__(name, parent)

    def data(self, column):
        r = super(ExtrudedSurfaceNode, self).data(column)

        return r

    def setData(self, column, value):
        super(ExtrudedSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return NodeType.ExtrudedSurfaceNode

    def resource(self):
        return ":/ruled_surface.png"


class SweepSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(SweepSurfaceNode, self).__init__(name, parent)
        self.sketchObject: Surface_Sweep = None

    def data(self, column):
        r = super(SweepSurfaceNode, self).data(column)
        if self.sketchObject:
            myGeometry = self.sketchObject.GetGeometry()
            myAISObject = self.sketchObject.GetAIS_Object()
        return r

    def setData(self, column, value):
        super(SweepSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return NodeType.SweepSurfaceNode

    def resource(self):
        return ":/sweep.png"


class ImportedSurfaceNode(SketchObjectNode):
    def __init__(self, name, parent=None):
        super(ImportedSurfaceNode, self).__init__(name, parent)

    def data(self, column):
        r = super(ImportedSurfaceNode, self).data(column)

        return r

    def setData(self, column, value):
        super(ImportedSurfaceNode, self).setData(column, value)

    def typeInfo(self):
        return NodeType.ImportedSurfaceNode
