# coding: utf-8

r"""Anchor Add Command"""

from os.path import join, dirname

import FreeCAD as App
import Part

from freecad_logging import info, debug, error
from anchor import Anchor, ViewProviderAnchor, make_anchor_feature
from vectors import perpendicular

if App.GuiUp:
    import FreeCADGui as Gui
else:
    msg_no_ui = "Adding an anchorable object requires the FreeCAD Gui to be up"
    error(msg_no_ui)


class CommandAnchorAdd:
    r"""AnchorAddCommand
    
    Command to add an anchor to a Part
    
    """
    def __init__(self):
        pass

    def Activated(self):
        r""""""
        debug("CommandAnchorAdd, Activated")

        # selection = Gui.Selection.getSelection()
        selection_ex = Gui.Selection.getSelectionEx()

        if len(selection_ex) != 1:
            msg = "Anchors : " \
                  "Select feature(s) on only 1 solid to add anchors to"
            error(msg)
            return
        else:
            # https://forum.freecadweb.org/viewtopic.php?t=7249
            unique_selection = selection_ex[0]
            selected_object = unique_selection.Object
            debug("  Selection : %s || %s" % (selected_object,
                                              selected_object.Shape.ShapeType))

            subselected_objects = unique_selection.SubObjects

            for subselected_object in subselected_objects:
                debug("SubSelection : %s || %s" % (subselected_object,
                                                   type(subselected_object)))
                # if isinstance(subselected_object, Part.Solid):
                #     debug("It is a Solid")
                # elif isinstance(subselected_object, Part.Shell):
                #     debug("It is a Shell")
                if isinstance(subselected_object, Part.Face):
                    debug("It is a Face")
                    face = subselected_object
                    u00, u10, v00, v10 = face.ParameterRange
                    u05 = (u00 + u10) / 2
                    v05 = (v00 + v10) / 2
                    p = face.valueAt(u05, v05)
                    u = face.normalAt(u05, v05)

                    v = perpendicular(u, normalize_=True, randomize_=False)

                    make_anchor_feature(p, u, v)

                elif isinstance(subselected_object, Part.Wire):
                    debug("It is a Wire")
                elif isinstance(subselected_object, Part.Edge):
                    debug("It is an Edge")
                    debug('TYPE : %s' % type(subselected_object.Curve))

                    if str(type(subselected_object.Curve)) == "<type 'Part.Circle'>":
                        debug("it is a circle")
                    elif str(type(
                            subselected_object.Curve)) == "<type 'Part.Line'>":
                        debug("it is a line")
                    else:
                        # known other possibilities
                        # -  <type 'Part.BSplineCurve'>
                        debug("it is NOT a circle and NOR a line")
                elif isinstance(subselected_object, Part.Vertex):
                    debug("It is a Vertex")
                else:
                    debug("What is that?")

        # a = App.ActiveDocument.addObject("App::FeaturePython", "Anchor")
        # Anchor(a)
        # ViewProviderAnchor(a.ViewObject)

    def GetResources(self):
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_add_anchor.svg")
        return {"MenuText": "Add anchor",
                "Accel": "Alt+C",
                "ToolTip": "Add an anchor to a part",
                "Pixmap": icon}

    def IsActive(self):
        r"""Determines if the command is active or inactive (greyed out)
        
        This method is called periodically, avoid calling other methods
        that print to the console

        """
        if App.ActiveDocument is None:
            return False
        else:
            return True
