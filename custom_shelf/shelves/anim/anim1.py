icon='BONE_DATA'
description = 'Ce code ne sert strictement à rien'

import bpy

variables =  {
'string' : 'toto',
'integer' : 1,
'float_value' : 0.5,
}




def main(variables) :

    print(variables['string'],variables['float_value'])

main(variables)
