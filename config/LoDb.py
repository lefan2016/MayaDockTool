# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------------#

_HEADER_        =       "_____________________________prsfxTools_____________________________"

_AUTHOR_        =       "Prana Ronita"
_PORTFOLIO_     =       "www.prsfx.net"
_EMAIL_         =       "prana.ronita@gmail.com / prsfx.net@gmail.com"
_SOCIAL_        =       "@prsfx"

_PROJECTNAME_   =       "LoDb"
_VERSION_       =       "1.2"

_ABOUT_         =       "© 2019 | Prana Ronita | @prsfx"
_LASTMODIFIED_  =       "15th December 2019"

_FOOTER_        =       "____________________________www.prsfx.net____________________________"

#-----------------------------------------------------------------------------------#

import LoDb

import os
import sys
import logging

import xml.etree.ElementTree as xml

from cStringIO import StringIO

#-----------------------------------------------------------------------------------#

_PyQt5message_    =   "default bind: PyQt5"
_PyQt4message_    =   "default bind: PyQt4"
_PySide2message_  =   "default bind: PySide2"
_PySideMessage_   =   "default bind: PySide2"
_nthngTbnd_       =   "Nothing to bind. Prolly nothin'."

#-----------------------------------------------------------------------------------#

defaultBind = "None"
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5 import uic, QtWidgets, QtCore, QtGui
    import sip
    logging.Logger.manager.loggerDict["PyQt5.uic.uiparser"].setLevel(logging.CRITICAL)
    logging.Logger.manager.loggerDict["PyQt5.uic.properties"].setLevel(logging.CRITICAL)
    defaultBind = _PyQt5message_
except:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        from PyQt4 import uic, QtGui
        import sip
        logging.Logger.manager.loggerDict["PyQt4.uic.uiparser"].setLevel(logging.CRITICAL)
        logging.Logger.manager.loggerDict["PyQt4.uic.properties"].setLevel(logging.CRITICAL)
        defaultBind = _PyQt4message_
    except:
        try:
            import xml.etree.ElementTree as xml
            from cStringIO import StringIO
            from PySide2.QtGui import *
            from PySide2.QtCore import *
            from PySide2.QtWidgets import *
            from PySide2 import QtGui
            from PySide2.QtUiTools import QUiLoader
            from PySide2.QtCore import QFile
            from PySide2.QtWidgets import QApplication, QMainWindow
            import pyside2uic as pysideuic
            import shiboken2 as shiboken
            logging.Logger.manager.loggerDict["pyside2uic.uiparser"].setLevel(logging.CRITICAL)
            logging.Logger.manager.loggerDict["pyside2uic.properties"].setLevel(logging.CRITICAL)
            defaultBind = _PySide2message_
        except:
            try:
                import xml.etree.ElementTree as xml
                from cStringIO import StringIO
                from PySide.QtGui import *
                from PySide.QtCore import *
                from PySide import QtGui
                import pysideuic, shiboken
                logging.Logger.manager.loggerDict["pysideuic.uiparser"].setLevel(logging.CRITICAL)
                logging.Logger.manager.loggerDict["pysideuic.properties"].setLevel(logging.CRITICAL)
                defaultBind = _PySideMessage_
            except:
                print _nthngTbnd_

print(defaultBind)

if defaultBind == _PyQt5message_:
    from PyQt5 import QtWidgets, QtCore, QtGui

elif defaultBind == _PySide2message_:
    from PySide2 import QtWidgets, QtCore, QtGui

#-----------------------------------------------------------------------------------#

def loadUiType( uiFile ):
    '''workaround to be able to load QT designer uis with both PySide and PyQt4'''
    # http://nathanhorne.com/guide-to-pyqtpyside/
    if defaultBind ==  "PyQt4":
        form_class, base_class =  uic.loadUiType( uiFile )
    else:
        parsed = xml.parse( uiFile )
        widget_class = parsed.find( 'widget' ).get( 'class' )
        form_class = parsed.find( 'class' ).text

        with open( uiFile, 'r' ) as f:
            o = StringIO()
            frame = {}

            pysideuic.compileUi( f, o, indent=0 )
            pyc = compile( o.getvalue(), '<string>', 'exec' )
            exec pyc in frame

            form_class = frame[ 'Ui_%s'%form_class ]
            base_class = eval( '%s'%widget_class )
    return form_class, base_class

#-----------------------------------------------------------------------------------#

def wrapinstance( ptr, base=None ):
    '''workaround to be able to wrap objects with both PySide and PyQt4'''
    # http://nathanhorne.com/pyqtpyside-wrap-instance/
    if ptr is None:
        return None
    ptr = long( ptr ) 
    if globals().has_key( 'shiboken' ):
        if base is None:
            qObj = shiboken.wrapInstance( long( ptr ), QObject )
            metaObj = qObj.metaObject()
            cls = metaObj.className()
            superCls = metaObj.superClass().className()
            if hasattr( QtGui, cls ):
                base = getattr( QtGui, cls )
            elif hasattr( QtGui, superCls ):
                base = getattr( QtGui, superCls ) 
            else:
                base = QWidget
        return shiboken.wrapInstance( long( ptr ), base )
    elif globals().has_key( 'sip' ):
        base = QObject
        return sip.wrapinstance( long( ptr ), base )
    else:
        return None

#-----------------------------------------------------------------------------------#
