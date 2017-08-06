#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

__author__="Hynek Lavicka"
__project__="HAL"

class general_HAL_class ():
    def __init__ ( self ):
        pass

    def InsertConfig(self, config):
        pass

    def WriteMemory ( self , address , content ):
        pass

    def ReadMemory ( self , address ):
        pass

    def GetInfo (self ):
        return { "name" : "general HAL" , "adresses": [] }

    def CompleteMemory ( self ):
        return {}
