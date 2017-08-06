#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

from unittest import TestCase

import sys
import unittest
import PySide.QtGui
import bitfield_widget
import support_functions
import HAL.local_memory_storage

app = PySide.QtGui.QApplication(sys.argv)

class TestBitfield_widget(TestCase):

    def setUp(self):
        self.config = support_functions.prepare_bitfield_dictionaries( "all_combinations.txt" )

        self.HAL_memory = HAL.local_memory_storage.local_memory_storage()

        self.HAL_memory.InsertConfig(self.config)

        # print ( "Config", self.config )
        self.bitfield_widget_inst = bitfield_widget.bitfield_widget ( self.config [ 0 ] , self.HAL_memory )

    def test_changeConfig(self):
        for item in self.config:
            self.bitfield_widget_inst.changeConfig ( item )
            # print("Config" , item)

            for count_widget , widget in enumerate ( self.bitfield_widget_inst.state_widgets ):
                supposed_type = None
                if item["bitfields"][count_widget]["width"] == 1:
                    supposed_type = PySide.QtGui.QPushButton
                elif 2 <= item["bitfields"][count_widget]["width"] <= 3:
                    supposed_type = PySide.QtGui.QComboBox
                    self.assertEqual ( widget.count () , 2 ** item["bitfields"][count_widget]["width"] )
                elif 4 <= item["bitfields"][count_widget]["width"]:
                    supposed_type = PySide.QtGui.QSlider
                    widget.setValue ( -1 )
                    self.assertEqual( widget.value () , 0 )

                    widget.setValue(10000)
                    self.assertEqual(widget.value(), 2 ** item["bitfields"][count_widget]["width"] -1 )
                else:
                    supposed_type = None

                # print ( type(widget) , supposed_type )
                self.assertEqual( type(widget) , supposed_type )

            for value in range (0 , 256):
                # print ( value )
                self.HAL_memory.WriteMemory ( item["address"] , value)
                self.bitfield_widget_inst.updateValueOfDisplays ( value )
                self.bitfield_widget_inst.updateValueOfInputs()
                self.bitfield_widget_inst.updateValue ()

                self.assertEqual( self.bitfield_widget_inst.lcd_decadic.value() , value )
                self.assertEqual( self.bitfield_widget_inst.lcd_octal.value() , value)
                self.assertEqual( self.bitfield_widget_inst.lcd_hexadecimal.value() , value)
                self.assertEqual( self.bitfield_widget_inst.lcd_binary.value() , value)

                for count_widget, widget in enumerate(self.bitfield_widget_inst.state_widgets):
                    # print ( count_widget , widget )
                    if item["bitfields"][count_widget]["width"] == 1:
                        mask = 1 << item["bitfields"][count_widget]["pos"]
                        state_value = value & mask
                        state = str(state_value >> item["bitfields"][count_widget]["pos"])
                        result = True if state == "1" else False

                        # print ( value , state , mask , widget.isChecked(), result )
                        self.assertEqual(widget.isChecked() , result)

                    if 2 <= item["bitfields"][count_widget]["width"] <= 3:
                        mask = 0
                        for position in range(item["bitfields"][count_widget]["width"]):
                            mask += 1 << (item["bitfields"][count_widget]["pos"] + position)

                        state_value = value & mask
                        state = state_value >> item["bitfields"][count_widget]["pos"]

                        # print ( widget.currentIndex() , state )
                        self.assertEqual( widget.currentIndex() , state)

                    if 4 <= item["bitfields"][count_widget]["width"]:
                        mask = 0
                        for position in range ( item["bitfields"][count_widget] [ "width" ] ):
                            mask += 1 << ( item["bitfields"][count_widget] [ "pos" ] + position )

                        state_value = value & mask
                        state = state_value >> item["bitfields"][count_widget] [ "pos" ]

                        # print ( widget.value(), state )
                        self.assertEqual ( widget.value(), state)

        self.su

if __name__ == "__main__":
    unittest.main()
