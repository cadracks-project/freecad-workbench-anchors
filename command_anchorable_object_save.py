# coding: utf-8

r"""Anchorable object save"""

from os.path import join, dirname

import FreeCAD as App
from PySide import QtGui

from freecad_logging import debug, error

if App.GuiUp:
    import FreeCADGui as Gui
else:
    msg_no_ui = "Saving an anchorable object requires the FreeCAD Gui to be up"
    error(msg_no_ui)


class CommandAnchorableObjectSave:
    r"""Anchorable object save command

    Command to write an anchorable object to a stepzip format

    """

    def __init__(self):
        pass

    def Activated(self):
        r"""The Save anchorable object Command was activated"""
        # selection = Gui.Selection.getSelection()
        selection_ex = Gui.Selection.getSelectionEx()

        debug("len selection_ex = %i" % len(selection_ex))

        if len(selection_ex) != 1:
            msg = "Anchors : " \
                  "Select only 1 anchorable object to save"
            error(msg)
            return
        else:
            # https://forum.freecadweb.org/viewtopic.php?t=7249
            unique_selection = selection_ex[0]
            selected_object = unique_selection.Object
            debug("  Selection : %s || %s" % (selected_object,
                                              selected_object.Shape.ShapeType))

            dialog = QtGui.QFileDialog.getSaveFileName(
                filter="Stepzip files (*.stepzip)")
            # todo : save logic
            #  check is anchorable object
            #  save shape as step
            #  save anchors file (+ feature attachment)
            #  zip it to a stepzip
            debug("Will save to %s" % str(dialog))

    def GetResources(self):
        r"""Resources for command integration in the UI"""
        icon = join(dirname(__file__),
                    "resources",
                    "freecad_workbench_anchors_save.png")
        return {"MenuText": "Save anchorable object",
                "Accel": "Ctrl+S",
                "ToolTip": "Save an anchorable object",
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
