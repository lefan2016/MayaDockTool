# -*- coding: utf-8 -*-

#-----------------------------------------------------------------------------------#

_PROJECTNAME_       =       "MayaDockWindow"
_AUTHOR_            =       "Prana Ronita / prsfx"
_TOOLFUNCTION_      =       "Create Polygon fron dropdown list nad open node editor."
_TOOLNAME_          =       "PTDW"
_TOOLVERSION_       =       "v0.0"

#-----------------------------------------------------------------------------------#

#How to use it?
    #In Maya script editor/shelf command tab, use:
'''

from myMayaTool import PolygonTool
PolygonTool.main()

'''

#-----------------------------------------------------------------------------------#

# import module
import os, sys
sys.dont_write_bytecode = True


# import tool name
import myMayaTool
import PolygonTool
reload(PolygonTool)


# import other/custom module
from config.LoDb import *
from config.LoDb import loadUiType
from config.LoDb import wrapinstance
''' You also can used default PySide2 or any other module here '''


from xml.etree import ElementTree as xml
from cStringIO import StringIO


# import maya module
from maya import mel as mel
from maya import cmds as cmds
from maya import OpenMayaUI as omui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

#-----------------------------------------------------------------------------------#

# custom and function
''' get path '''
myPath              =   os.path.dirname(__file__)


''' get maya window '''
def mayaMainWindow():
    mainWindowPtr   =   omui.MQtUtil.mainWindow()
    return wrapinstance(long(mainWindowPtr), QtWidgets.QWidget)


''' check if it's Maya '''
def isMaya():
    try:
        cmds.about(batch=True)
        return True
    except ImportError:
        return False

#-----------------------------------------------------------------------------------#

# PolygonToolDockWindow ui file setup a.k.a. ptdw
''' look up for ui file '''
ptdw_form, ptdw_base    =   loadUiType(myPath + "/layout/ptdw_interface.ui")


# Maya mixin window tool name
''' naming your tool '''
PolygonToolDock_WindowName   =   "PTDW " + _TOOLVERSION_


# ptdw window class
class ptdwUI(ptdw_form, ptdw_base):
    def __init__(self, parent=None):
        super(ptdwUI, self).__init__(parent)

        self.setupUi(self)

        #show status bar message
        self.statusbar.showMessage("Hi, I'm PTDW " + _TOOLVERSION_)

        #set node editor icon
        neIco = QIcon(myPath + "/icon/nodeEditor_icon.png")
        self.nodeEditor_pbttn.setIcon(neIco)


        #_INPUT_METHOD_#
        ''' this section is to input your method before signal it to Maya '''

        # create polygon fromlist
        self.createPoly_pbttn.clicked.connect(self.__createPolyFromList)

        # show node editor
        self.nodeEditor_pbttn.clicked.connect(self.__showNodeEditor)



    #_OUTPUT_METHOD_#
    ''' output function from input method '''

    # create polygon fromlist
    def __createPolyFromList(self, *args):
        # first, let's assign our combo box
        polyList = self.polygonList_cmbbx.currentText()
        '''
        you also can use .currentIndex() if that suit you
        '''

        if polyList == "Sphere":
            #do this
            cmds.polySphere()

        elif polyList == "Cube":
            #do this
            cmds.polyCube()

        elif polyList == "Cylinder":
            #do this
            cmds.polyCylinder()

        elif polyList == "Cone":
            #do this
            cmds.polyCone()

        else:
            #give warning message
            cmds.warning("There's no such thing like that.")


    def __showNodeEditor(self, *args):
        mel.eval("NodeEditorWindow;")


    def closeEvent(self, *args):
        self.parent().close()

#-----------------------------------------------------------------------------------#

''' Okay, so now we want to able to dock it inside maya window '''
# ptdw mixin class
class ptdwMixinDock(MayaQWidgetDockableMixin, PolygonTool.ptdwUI):
    ''' mixinWindowName(MayaQWidgetDockableMixin, TooName.ToolUIname) '''

    ptdw_toolName = PolygonToolDock_WindowName

    def __init__(self, parent=None):
        # create delete instances
        self.deleteInstances()

        super(ptdwMixinDock, self).__init__(parent)

        # get maya window
        mayaMainWindow()

        # set window name
        self.setWindowTitle(PolygonToolDock_WindowName)

        # set window flags
        self.setWindowFlags(QtCore.Qt.Window)

        # delete the pointer when widget closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)




    # trigger close event
    def dockCloseEventTriggered(self, *args):
        self.deleteInstances()

    # delete instances
    def deleteInstances(self, *args):
        for obj in mayaMainWindow().children():
            if str(type(obj)) == ptdwMixinDock:
                if obj.widget().objectName() == self.__class__.ptdw_toolName:
                    print 'Deleting instance {0}'.format(obj)
                    mayaMainWindow().removeDockWidget(obj)
                    obj.setParent(None)
                    obj.deleteLater()

    # delete control workspace
    def deleteControl(self, control):

        if cmds.workspaceControl(control, q=True, exists=True):
            cmds.workspaceControl(control, e=True, close=True)
            cmds.deleteUI(control, control=True)

    # now set how to run it
    def run(self):
        self.setObjectName(PolygonToolDock_WindowName)

        workspaceControlName = self.objectName() + "WorkspaceControl"
        self.deleteControl(workspaceControlName)

        self.show(dockable=True, floating=True)
        # raise window to top
        self.raise_()

#-----------------------------------------------------------------------------------#

''' do right here to launch the UI '''

def launch():
    # let's import about log from function folder
    import function.aboutPolygonTool as abpt
    abpt.about()

    ptdwMixinWindow = ptdwMixinDock()
    ptdwMixinWindow.run()

    return ptdwMixinWindow

def main(*args, **kwargs):
    if PolygonTool.isMaya():
        launchPTDW = launch()

    return launchPTDW

if __name__ == "__main__":
    with PolygonTool.app():
        PolygonTool.main()
