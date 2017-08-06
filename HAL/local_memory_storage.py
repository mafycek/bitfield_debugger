#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

__author__="Hynek Lavicka"
__project__="HAL"

from . import general_HAL

class local_memory_storage ( general_HAL.general_HAL_class ):
    def __init__ ( self ):
        super().__init__()
        self.config = None
        self.memory = None

    def InsertConfig ( self , config ):
        self.config = config

        self.memory = {}
        for item in self.config:
            self.memory [ item ["address"] ] = int ( 0 )

    def WriteMemory ( self , address , content ):
        if address in self.memory:
            self.memory [ address ] = content
            return True
        else:
            return False

    def ReadMemory ( self , address ):
        if address in self.memory:
            return self.memory [ address ]
        else:
            return None

    def GetInfo ( self ):
        return { "name" : "general HAL" , "adresses": self.memory.keys() }

    def CompleteMemory ( self ):
        return self.memory
