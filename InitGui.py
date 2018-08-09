# coding : utf-8

r"""InitGui.py is loaded when FreeCAD runs in GUI mode"""


class AnchorWorkbench(Gui.Workbench):
    """
    class which gets initiated at startup of the gui
    """

    # The workbench name as it appears in the workbenches list
    MenuText = "Anchors"
    ToolTip = "Anchors based assembly"
    user_app_data = App.getUserAppDataDir()
    # Msg("User app data dir : %s\n" % user_app_data)
    Icon = user_app_data + "Mod/FreeCAD-Anchors/resources/default_icon.svg"

    def GetClassName(self):
        return "Gui::PythonWorkbench"

    def Initialize(self):
        """This function is called at the first activation of the workbench.
        here is the place to import all the commands
        """
        Msg("Anchor workbench initialize\n")

        from command_anchor_add import CommandAnchorAdd
        from command_assembly_add import CommandAssemblyAdd

        commands = {"AnchorAdd": CommandAnchorAdd(),
                    "AssemblyAdd": CommandAssemblyAdd()}

        for k, v in commands.items():
            FreeCADGui.addCommand(k, v)

        # creates a new toolbar with your commands
        self.appendToolbar("Anchors commands toolbar", commands.keys())

        # creates a new menu
        self.appendMenu("Anchors", commands.keys())

        # appends a submenu to an existing menu
        # not useful in the Anchors Workbench context
        # self.appendMenu(["Tools", "My submenu"], commands.keys())

    def Activated(self):
        r"""code which should be computed when a user
        switches to this workbench"""
        Msg("Anchor workbench activated\n")

    def Deactivated(self):
        r"""code which should be computed when this workbench is deactivated"""
        Msg("Anchor workbench activated\n")


Gui.addWorkbench(AnchorWorkbench())
