#!/usr/bin/env python3

# Developed by Hynek Lavicka (C) 2017, h.lavicka@email.cz
# Temporary resting of the application is allowed by the author.
# Use, modification and development of the program is allowed by the author

import sys

def find_pattern_in_list_of_lines ( list_of_lines , pattern ):
    for number, line in enumerate(list_of_lines):
        if pattern in line:
            return number
    return None

def create_info_register_dict ( list_of_lines ):
    register = {}
    accepted_keywords = [ "name" , "address" , "value" ]

    for count in range ( len ( accepted_keywords) ):
        split = list_of_lines [ count ].split ( ":" )
        if "name" in split[0]:
            split[1] = split[1].replace('"', "")

        register [ split [ 0 ] ] = split [ 1 ]

    register [ "bitfields" ] = []

    index = find_pattern_in_list_of_lines ( list_of_lines , "bitfields:{" )
    list_of_lines_bitfields = list_of_lines [ index + 1 : ]

    index = find_pattern_in_list_of_lines( list_of_lines_bitfields , "bitfield" )
    # print ( index )
    list_of_lines_bitfields = list_of_lines_bitfields [ index + 1 : ]

    while index is not None:
        index_new = find_pattern_in_list_of_lines(list_of_lines_bitfields, "bitfield")

        list_to_be_parsed = list_of_lines_bitfields [ : index_new ]

        new_dictionary = {}
        for count in range(3):
            split = list_to_be_parsed[count].split(":")
            if "name" in split [ 0 ]:
                split [ 1 ] = split [ 1 ].replace ( '"' , "" )
            if ( "pos" in split [ 0 ] ) or ( "width" in split [ 0 ] ):
                split[1] = int ( split[1] )
            new_dictionary[split[0]] = split[1]

        register["bitfields"].append ( new_dictionary )

        if index_new is not None:
            list_of_lines_bitfields = list_of_lines_bitfields [ index_new + 1 : ]

        index = index_new

    return register

def prepare_bitfield_dictionaries ( file ):
    configuration = []

    with open ( file , "rt" ) as fh:
        for line in fh:
            configuration .append ( line.replace( "\n" , "" ).replace( " " , "" ) )

    # print (configuration)
    index = find_pattern_in_list_of_lines ( configuration , "device" )

    rest_configuration = configuration [ index + 1 : ]
    # print (index , rest_configuration )

    devices = []

    index = find_pattern_in_list_of_lines( rest_configuration , "register")
    # print ( index )
    rest_configuration_device = rest_configuration [ index + 1 :]
    while index is not None:

        index_new = find_pattern_in_list_of_lines( rest_configuration_device , "register")
        if index_new is not None:
            devices.append ( rest_configuration_device [ : index_new ] )
            rest_configuration_device = rest_configuration_device [ index_new + 1 : ]
        else:
            devices.append(rest_configuration_device[:])

        index = index_new

        # print(index, index_new , rest_configuration_device)

    # print ( "Devices:" , devices )

    devices_dictionary = []
    for item in devices:
        devices_dictionary.append ( create_info_register_dict ( item ) )

    return ( devices_dictionary )


def subset_sum ( target, partial=[], partial_sum=0):
    if partial_sum == target:
        yield partial
    if partial_sum >= target:
        return
    for i in range ( 1 , target + 1 ):
        yield from subset_sum ( target, partial + [i], partial_sum + i)

def PrepareAllCombinations ( filename ):
    with open ( filename , "wt" ) as fh:
        print ( "device" , file = fh )
        finish = False

        for count , item in enumerate ( subset_sum(8) ):
            print(item)
            print ( "register" , file = fh )
            print ( "name: reg" + str (count) , file=fh )
            print ( "address:" + "{0:04d}".format(count) , file = fh )
            print ( "value: 0-255" , file = fh )
            print ( "bitfields: {", file=fh )
            bit_number = 0
            for count_width , width in enumerate( item ):
                print("bitfield", file=fh)
                print("name: bit" + str(bit_number) , file=fh)
                print("pos:" + str(bit_number) , file=fh )
                print("width:" + str(width), file=fh)
                bit_number += width
            print ( "}", file=fh )



if __name__ == '__main__':
    prepare_bitfield_dictionaries ( "definition.txt" )

    for item in subset_sum (8 ):
        print ( item )

    PrepareAllCombinations( "all_combinations.txt" )