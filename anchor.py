# coding: utf-8

r"""Anchor Python Feature

Is made of a point and 2 unit and orthogonal vectors

"""

import FreeCAD as App

from pivy import coin


class Anchor:
    def __init__(self, obj):
        obj.addProperty("App::PropertyVector",
                        "p",
                        "Definition",
                        "Anchor's origin").p = App.Vector(0, 0, 0)
        obj.addProperty("App::PropertyVector",
                        "u",
                        "Definition",
                        "Anchor's u vector").u = App.Vector(1, 0, 0)
        obj.addProperty("App::PropertyVector",
                        "v",
                        "Definition",
                        "Anchor's v vector").v = App.Vector(0, 1, 0)
        obj.Proxy = self

    def onChanged(self, fp, prop):
        r"""Do something when a property has changed"""
        App.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        r"""Do something when doing a recomputation, this method is mandatory"""
        App.Console.PrintMessage("Recompute Anchor feature\n")


class ViewProviderAnchor:
    def __init__(self, obj):
        r"""Set this object to the proxy object of the actual view provider"""
        obj.addProperty("App::PropertyColor",
                        "Color",
                        "Anchor",
                        "Color of the anchor").Color = (0.0, 0.0, 1.0)
        obj.Proxy = self

    def attach(self, obj):
        r"""Setup the scene sub-graph of the view provider,
        this method is mandatory
        """
        self.shaded = coin.SoGroup()
        self.wireframe = coin.SoGroup()

        self.scale = coin.SoScale()
        self.color = coin.SoBaseColor()
        self.transform = coin.SoTransform()

        self.transform.translation.setValue((0, 5, 0))
        self.transform.center.setValue((0, 0, 0))
        import math
        self.transform.rotation.setValue(coin.SbVec3f((1, 0, 0)), math.pi/2)

        # data = coin.SoCube()
        cone = coin.SoCone()
        cone.height.setValue(1)

        self.shaded.addChild(self.transform)
        self.shaded.addChild(self.scale)
        self.shaded.addChild(self.color)
        self.shaded.addChild(cone)
        obj.addDisplayMode(self.shaded, "Shaded")

        style = coin.SoDrawStyle()
        style.style = coin.SoDrawStyle.LINES
        self.wireframe.addChild(style)
        self.wireframe.addChild(self.transform)
        self.wireframe.addChild(self.scale)
        self.wireframe.addChild(self.color)
        self.wireframe.addChild(cone)
        obj.addDisplayMode(self.wireframe, "Wireframe")

        self.onChanged(obj, "Color")

    def updateData(self, fp, prop):
        r"""If a property of the handled feature has changed,
        we have the chance to handle this here
        """
        # fp is the handled feature,
        # prop is the name of the property that has changed
        # l = fp.getPropertyByName("Length")
        # w = fp.getPropertyByName("Width")
        # h = fp.getPropertyByName("Height")
        # self.scale.scaleFactor.setValue(float(l), float(w), float(h))
        pass

    def getDisplayModes(self, obj):
        r"""Return a list of display modes"""
        modes = ["Shaded", "Wireframe"]
        return modes

    def getDefaultDisplayMode(self):
        r"""Return the name of the default display mode.
        It must be defined in getDisplayModes."""
        return "Shaded"

    def setDisplayMode(self, mode):
        r"""Map the display mode defined in attach with those
        defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional
        """
        return mode

    def onChanged(self, vp, prop):
        r"""Here we can do something when a single property got changed"""
        App.Console.PrintMessage("Change property: " + str(prop) + "\n")
        if prop == "Color":
            c = vp.getPropertyByName("Color")
            self.color.rgb.setValue(c[0], c[1], c[2])

    def getIcon(self):
        r"""Return the icon in XPM format which will appear in the tree view.
        This method is\ optional and if not defined a default icon is shown.
        """
        return """
            /* XPM */
            static const char * ViewProviderBoat_xpm[] = {
            "16 16 6 1",
            "   c None",
            ".  c #141010",
            "+  c #615BD2",
            "@  c #C39D55",
            "#  c #000000",
            "$  c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        r"""When saving the document this object gets stored using
        Python's json module.
        Since we have some un-serializable parts here -- the Coin stuff --
        we must define this method to return a tuple of all serializable objects
        or None
        """
        return None

    def __setstate__(self, state):
        r"""When restoring the serialized object from document we have
        the chance to set some internals here.
        Since no data were serialized nothing needs to be done here.
        """
        return None