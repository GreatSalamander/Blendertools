
import bpy

variables =  {
'string' : 'toto',
'integer' : 1,
'float_value' : 0.5,
'object' : bpy.context.object,
'data' : bpy.context.object.data,
'scene' : bpy.context.scene,
'list' : bpy.context.selected_objects,


}




def main(variables) :

    print(variables['string'],variables['object'])

main(variables)
