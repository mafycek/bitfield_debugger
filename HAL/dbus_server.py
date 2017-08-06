#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

__author__="Hynek Lavicka"
__project__="HAL"

import dbus
import dbus.service
import dbus.mainloop.glib
import gi.repository.GLib

import yaml

class dbus_server (dbus.service.Object):
    def __init__ ( self ):
        super().__init__()
        self.config = None
        self.memory = None

    @dbus.service.method("com.service.memory", in_signature='s', out_signature='')
    def InsertConfig ( self , config ):
        self.config = yaml.load ( config )
        # print ( self.config )

        self.memory = {}
        for item in self.config:
            self.memory [ item ["address"] ] = int ( 0 )

    @dbus.service.method("com.service.memory", in_signature='si', out_signature='b')
    def WriteMemory ( self , address , content ):
        # print ( address , content )
        if address in self.memory:
            self.memory [ address ] = content
            return True
        else:
            return False

    @dbus.service.method("com.service.memory", in_signature='s', out_signature='i')
    def ReadMemory ( self , address ):
        # print ( address )
        if address in self.memory:
            return self.memory [ address ]
        else:
            return -1

    @dbus.service.method("com.service.memory", in_signature='', out_signature='s')
    def GetInfo ( self ):
        return yaml.dump ( { "name" : "general HAL" , "adresses": self.memory.keys() } )

    @dbus.service.method("com.service.memory", in_signature='', out_signature='s')
    def CompleteMemory ( self ):
        return yaml.dump ( self.memory )

    def run(self):
        dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        bus_name = dbus.service.BusName("com.service.memory", dbus.SessionBus())
        dbus.service.Object.__init__(self, bus_name, "/")

        self._loop = gi.repository.GLib.MainLoop ()

        print ( "Service running..." )

        self._loop.run()
        print ( "Service stopped" )

if __name__ == '__main__':
   server = dbus_server ()
   server.run()