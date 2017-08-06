#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

import sys

import bitfield_widget
import PySide.QtGui
import support_functions
import HAL.local_memory_storage
import HAL.dbus_client

class bitfield_debugger ( PySide.QtGui.QMainWindow ):
    def __init__(self , filename , currentHAL = None ):
        super().__init__()
        self.HAL = currentHAL
        self.bitfield_widget = None
        self.list_of_configurations = support_functions.prepare_bitfield_dictionaries ( filename )

        self.HAL.InsertConfig ( self.list_of_configurations )

        self.centralWidget = PySide.QtGui.QWidget( )

        self.combo_register = PySide.QtGui.QComboBox ( self )
        self.write_memory_button = PySide.QtGui.QPushButton ( self.tr ( "Write memory" ) , self )
        if self.HAL is None:
            self.write_memory_button.setDisabled( True )

        self.bitfield_widget = bitfield_widget.bitfield_widget ( self.list_of_configurations[self.combo_register.currentIndex()], self.HAL, parent=self )

        self.write_memory_button.clicked.connect ( self.bitfield_widget.writeMemory )

        self.grid_box_layout = PySide.QtGui.QGridLayout()
        self.grid_box_layout.addWidget ( self.combo_register , 0 , 0 , 1 , 1 )
        self.grid_box_layout.addWidget ( self.write_memory_button , 1 , 0 , 1 , 1 )
        self.grid_box_layout.addWidget ( self.bitfield_widget , 0 , 1 , 2 , 1 )

        for number , item_register in enumerate ( self.list_of_configurations ):
            text =  self.tr("Name: ") + str ( item_register ["name"] ) + " " + self.tr("Address: ") + str ( item_register [ "address" ] )
            self.combo_register.addItem ( text , number )

        self.combo_register.setCurrentIndex ( 0 )
        self.combo_register.currentIndexChanged.connect ( self.changeBitfieldWidget )

        self.changeBitfieldWidget ( self.combo_register.currentIndex() )

        self.centralWidget.setLayout( self.grid_box_layout )

        self.setCentralWidget(self.centralWidget)

    @PySide.QtCore.Slot(int)
    def changeBitfieldWidget ( self , value):
        # print ("changeBitfieldWidget")
        # print ( self.list_of_configurations [ self.combo_register.currentIndex() ] )

        self.bitfield_widget.changeConfig ( self.list_of_configurations [ self.combo_register.currentIndex() ] )


if __name__ == '__main__':

    device = "definition.txt"
    if len(sys.argv) > 1:
        device = sys.argv [ 1 ]

    HAL_used=None
    if len(sys.argv) > 2 and "dbus" in sys.argv[2]:
        HAL_dbus_memory = HAL.dbus_client.dbus_client ( )
        HAL_used = HAL_dbus_memory
    else:
        HAL_memory = HAL.local_memory_storage.local_memory_storage ( )
        HAL_used = HAL_memory

    language = None
    if len(sys.argv) > 3:
        language = sys.argv[3]

    app = PySide.QtGui.QApplication(sys.argv)

    if language is not None:
        translator = PySide.QtCore.QTranslator()
        translator.load( language )
        app.installTranslator(translator)

    view = bitfield_debugger ( device , HAL_used )

    view.show ()

    sys.exit ( app.exec_ ( ) )
