#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

import PySide.QtCore
import PySide.QtGui
import sys
import support_functions
import HAL

class bitfield_widget ( PySide.QtGui.QGroupBox ):
    currentValueChanged = PySide.QtCore.Signal( int )

    def __init__(self , config , current_HAL , parent = None ):
        super().__init__ ( )

        # print (config)
        self.config = config
        self.HAL = current_HAL

        self.bitfield_value = self.getValueOfMemory ()

        # self.setTitle( self.tr ( "Bitfield " ) + self.config [ "name" ] )
        self.setToolTip ( self.tr ( "Widget for manipulating of bitfield " ) + self.config [ "name" ] )

        self.label_value = PySide.QtGui.QLabel ( self )
        self.label_value.setToolTip ( self.tr ( "Memory address of the bitfield" ) )

        self.lcd_decadic = PySide.QtGui.QLCDNumber ( 3 , self )
        self.lcd_binary = PySide.QtGui.QLCDNumber ( 8 , self )
        self.lcd_hexadecimal = PySide.QtGui.QLCDNumber ( 2 , self )
        self.lcd_octal = PySide.QtGui.QLCDNumber( 3 , self)

        self.lcd_decadic.setToolTip( self.tr ("Decadic value") )
        self.lcd_binary.setToolTip(self.tr("Binary value"))
        self.lcd_hexadecimal.setToolTip(self.tr("Hexadecimal value"))
        self.lcd_octal.setToolTip(self.tr("Octal value"))

        self.lcd_binary.setBinMode ( )
        self.lcd_hexadecimal.setHexMode ( )
        self.lcd_octal.setOctMode ( )

        self.updateValueOfDisplays ( self.bitfield_value )

        self.label_modificators = PySide.QtGui.QLabel ( self.tr ("Modificators of bitfield") , self )
        self.label_modificators.setToolTip ( self.tr ("Modificators of bitfield") )

        self.state_widgets = []

        self.vbox = PySide.QtGui.QVBoxLayout()
        self.vbox.addWidget ( self.label_value )
        self.vbox.addWidget ( self.lcd_decadic )
        self.vbox.addWidget ( self.lcd_binary )
        self.vbox.addWidget ( self.lcd_hexadecimal )
        self.vbox.addWidget ( self.lcd_octal )
        self.vbox.addWidget ( self.label_modificators )

        self.changeConfig ( self.config )

        self.setLayout(self.vbox)


    def getValueOfMemory ( self ):
        if self.HAL is not None:
            bitfield_value = self.HAL.ReadMemory ( self.config [ "address" ] )

            if bitfield_value is None:
                msgBox = PySide.QtGui.QMessageBox ()
                msgBox.setText ( self.tr ("The memory at address {} cannot be read").format ( self.config [ "address" ] ) )
                msgBox.setInformativeText( self.tr ( "Default value would be used instead." ) )
                msgBox.setStandardButtons ( PySide.QtGui.QMessageBox.Ok )
                msgBox.setDefaultButton ( PySide.QtGui.QMessageBox.Ok )
                value = msgBox.exec_ ()
                bitfield_value = 0

        else:
            msgBox = PySide.QtGui.QMessageBox()
            msgBox.setText(self.tr("HAL is not set"))
            msgBox.setInformativeText(self.tr("Reading/Writing operations are not performed"))
            msgBox.setStandardButtons(PySide.QtGui.QMessageBox.Ok)
            msgBox.setDefaultButton(PySide.QtGui.QMessageBox.Ok)
            value = msgBox.exec_()
            bitfield_value = 0

            self.setDisabled()

        return bitfield_value

    @PySide.QtCore.Slot(dict)
    def changeConfig ( self , config ):
        for widget in self.state_widgets:
            self.layout().removeWidget ( widget )
            widget.setParent ( None )

        self.config = config

        self.setTitle(self.tr("Bitfield ") + self.config["name"])
        self.label_value.setText( self.tr ("Address: ") + config [ "address" ] )

        self.readMemory()

        for item in self.state_widgets:
            self.vbox.addWidget(item)

    def readMemory ( self ):
        self.bitfield_value = self.getValueOfMemory()
        self.updateValueOfDisplays(self.bitfield_value)
        self.updateValueOfInputs ()

    @PySide.QtCore.Slot()
    def writeMemory ( self ):
        if self.HAL is not None:
            self.HAL.WriteMemory ( self.config [ "address" ] , self.bitfield_value )

    def updateValueOfInputs ( self ):
        self.state_widgets = []
        for item in self.config [ "bitfields" ]:
            if item [ "width" ] == 1:
                mask = 1 << item [ "pos" ]
                state_value = self.bitfield_value & mask
                state = str ( state_value >> item [ "pos" ] )

                button = PySide.QtGui.QPushButton ( self.tr("Bit: ") + str ( item [ "pos" ] ) + " " + self.tr("State: ") + str ( state ) , self)
                button.setToolTip ( self.tr ( "My button" ) )
                button.setCheckable ( True )
                button.setChecked ( True if state == "1" else False )

                button.toggled.connect ( self.updateValue )

                self.state_widgets.append ( button )

            if 2 <= item [ "width" ] <= 3:
                mask = 0
                for position in range ( item [ "width" ] ):
                    mask += 1 << ( item [ "pos" ] + position )

                state_value = self.bitfield_value & mask
                state = state_value >> item [ "pos" ]

                combo = PySide.QtGui.QComboBox(self)
                combo.setToolTip(self.tr("My combo"))
                for item_number_combo in range ( 2 ** item [ "width" ] ):
                    combo_text = ""
                    for position in range(item["width"]):
                        mask = 1 << position
                        state_bit = ( item_number_combo & mask ) >> position
                        combo_text += self.tr("B: ") + str ( item [ "pos" ] + position ) + self.tr(" S: ") + str ( state_bit ) + "; "

                    combo.addItem( str ( combo_text ) , str ( item_number_combo ) )

                # combo.setCurrentIndex ( combo.findData( str ( state ) ) )
                combo.setCurrentIndex(state)

                combo.currentIndexChanged.connect ( self.updateValue )

                self.state_widgets.append ( combo )

            if 4 <= item["width"]:
                mask = 0
                for position in range ( item [ "width" ] ):
                    mask += 1 << ( item [ "pos" ] + position )

                state_value = self.bitfield_value & mask
                state = state_value >> item [ "pos" ]

                slider = PySide.QtGui.QSlider(PySide.QtCore.Qt.Orientation(PySide.QtCore.Qt.Orientation.Horizontal), self)
                slider.setToolTip (self.tr("My super slider"))
                slider.setMinimum ( 0 )
                slider.setMaximum ( ( 2 ** item["width"] ) - 1 )
                slider.setTickPosition( PySide.QtGui.QSlider.TicksBothSides )

                slider.setValue( state )

                slider.valueChanged.connect ( self.updateValue )

                self.state_widgets.append ( slider )


            # slot
    @PySide.QtCore.Slot ( )
    @PySide.QtCore.Slot ( int )
    def updateValue ( self ):
        number = 0
        for item_widget , item_config in zip ( self.state_widgets , self.config [ "bitfields" ] ):
            if item_config [ "width" ] == 1:
                state = 1 if item_widget.isChecked () else 0
                number += state << item_config [ "pos" ]
                item_widget.setText ( self.tr("Bit: ") + str ( item_config [ "pos" ] ) + " " + self.tr("State: ") + str ( state ) )

            if 2 <= item_config["width"] <= 3:
                number += item_widget.currentIndex () << item_config [ "pos" ]

            if 4 <= item_config["width"]:
                number += item_widget.sliderPosition () << item_config [ "pos" ]

        self.updateValueOfDisplays ( number )


    @PySide.QtCore.Slot(int)
    def updateValueOfDisplays ( self , value ):
        self.bitfield_value = value
        self.lcd_decadic.display ( self.bitfield_value )
        self.lcd_binary.display ( self.bitfield_value )
        self.lcd_hexadecimal.display ( self.bitfield_value )
        self.lcd_octal.display ( self.bitfield_value)


if __name__ == '__main__':
    list_of_configurations = support_functions.prepare_bitfield_dictionaries( "definition.txt" )

    print ( list_of_configurations [ 0 ] )

    app = PySide.QtGui.QApplication ( sys.argv )

    # translator = PySide.QtCore.QTranslator()
    # translator.load('cz_CZ')
    # app.installTranslator(translator)

    view = bitfield_widget( "Můj grupáč" , list_of_configurations [ 0 ] )

    view.show ()

    sys.exit ( app.exec_ ( ) )
