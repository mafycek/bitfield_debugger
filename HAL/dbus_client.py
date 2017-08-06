#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

__author__="Hynek Lavicka"
__project__="HAL"

from . import general_HAL
# import general_HAL
import dbus
import yaml

class dbus_client ( general_HAL.general_HAL_class ):
    def __init__ ( self ):
        super().__init__()

        try:
            bus = dbus.SessionBus()
            sys_bus = dbus.SystemBus()

            service = bus.get_object('com.service.memory', "/")
            interface = dbus.Interface(service, 'com.service.memory')

            self.InsertConfig_dbus = service.get_dbus_method ( 'InsertConfig', 'com.service.memory' )
            self.WriteMemory_dbus = service.get_dbus_method ( 'WriteMemory', 'com.service.memory' )
            self.ReadMemory_dbus = service.get_dbus_method ( 'ReadMemory', 'com.service.memory')
            self.GetInfo_dbus = service.get_dbus_method('GetInfo', 'com.service.memory')
            self.CompleteMemory_dbus = service.get_dbus_method('CompleteMemory', 'com.service.memory')

        except BaseException as exc:
            self.ProblemWithDbusHandler()

    def InsertConfig ( self , config ):
        self.config = config

        try:
            # print ( yaml.dump( self.config ) )
            self.InsertConfig_dbus ( yaml.dump( self.config ) )
        except BaseException as exc:
            self.ProblemWithDbusHandler()

    def WriteMemory ( self , address , content ):
        try:
            return self.WriteMemory_dbus( address , content )
        except BaseException as exc:
            self.ProblemWithDbusHandler()

    def ReadMemory ( self , address ):
        try:
            value = self.ReadMemory_dbus ( address )
        except BaseException as exc:
            value = -1
            self.ProblemWithDbusHandler()
        finally:
            if value == -1:
                return None
            else:
                return value

    def GetInfo ( self ):
        try:
            return yaml.load( self.GetInfo_dbus ( ) )
        except BaseException as exc:
            self.ProblemWithDbusHandler()

    def CompleteMemory ( self ):
        try:
            return yaml.load( self.CompleteMemory_dbus ( ) )
        except BaseException as exc:
            self.ProblemWithDbusHandler()

    def ProblemWithDbusHandler ( self, exc ):
        print ( self.tr ("Problem with DBUS session") , exc )

if __name__ == '__main__':
    import sys
    from pathlib import Path

    sys.path.append(str(Path('.').absolute().parent))
    import support_functions

    list_of_configurations = support_functions.prepare_bitfield_dictionaries ( "../definition.txt" )

    client = dbus_client ()
    client.InsertConfig ( list_of_configurations )
    print ( client.WriteMemory ( "0x0001" , 2 ) )
    print ( client.ReadMemory( "0x0001" ) )
    print ( client.CompleteMemory() )

