# coding: utf-8

r"""Anchor Add Command"""

from os.path import join, dirname

import FreeCAD as App
import FreeCADGui as Gui

import Part


from freecad_logging import info, debug, error
from anchor import Anchor, ViewProviderAnchor


class CommandAnchorAdd:
    r"""AnchorAddCommand
    
    Command to add an anchor to a Part
    
    """
    def __init__(self):
        pass

    def Activated(self):
        r""""""
        info("This command will, in the future, add an anchor to a Part")

        # selection = Gui.Selection.getSelection()
        selection_ex = Gui.Selection.getSelectionEx()
        # debug("  Selection : %s" % str(selection))
        # debug("Selection Ex: %s" % str(selection_ex))

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
                if isinstance(subselected_object, Part.Face):
                    debug("It is a Face")
                elif isinstance(subselected_object, Part.Edge):
                    debug("It is an Edge")
                elif isinstance(subselected_object, Part.Vertex):
                    debug("It is a Vertex")
                else:
                    debug("What is that?")

        a = App.ActiveDocument.addObject("App::FeaturePython", "Anchor")
        Anchor(a)
        ViewProviderAnchor(a.ViewObject)

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
