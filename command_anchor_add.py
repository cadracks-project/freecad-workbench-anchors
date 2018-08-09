# coding: utf-8

r"""Anchor Add Command"""

from os.path import join, dirname

import FreeCAD as App

from freecad_logging import info


class CommandAnchorAdd:
    r"""AnchorAddCommand
    
    Command to add an anchor to a Part
    
    """
    def __init__(self):
        pass

    def Activated(self):
        r""""""
        info("This command will, in the future, add an anchor to a Part")

    def GetResources(self):
        icon = join(dirname(__file__), "resources", "default_icon.svg")
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
