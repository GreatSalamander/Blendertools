import bpy
from mathutils import Vector,Matrix
from math import sqrt
import numpy

MASTER_bones = []
SCALE_bones = []
armature = bpy.context.active_object.data

def between(a,b,c):
    
    C = bpy.context
    D = bpy.data
    
    print((b-a).dot(c-a))
    print(numpy.linalg.norm(b-a)**2)
    
    if ( round((b-a).cross(c-a).length,5) == 0.0 and (  0 <= (b-a).dot(c-a) <= numpy.linalg.norm(a-b)**2 ) ) or a==c or b==c:
        return(1- c.cross(b).length / a.cross(b).length)
    else:
        return(False)

for bone in bpy.context.active_object.data.edit_bones :
    if bone.name.startswith("MASTER") :
        
        MASTER_bones.append(bone)
        
    else :
        
        SCALE_bones.append(bone)

for bone in SCALE_bones :
    
    try:
        del(bone["head"])
        del(bone["headParent"])
        del(bone["tail"])
        del(bone["tailParent"])
        del(bone["roll"])
    except KeyError:
        pass

    for masterBone in MASTER_bones :
        
        bHead = between(masterBone.head,masterBone.tail,bone.head)
        bTail = between(masterBone.head,masterBone.tail,bone.tail)
        
        if type(bHead)!= type(False):
            bone["head"] = bHead
            bone["headParent"]= masterBone.name
            bone["roll"]= masterBone.roll - bone.roll
           
        if type(bTail)!= type(False):
            bone["tail"] = bTail
            bone["tailParent"]= masterBone.name
            bone["roll"]= masterBone.roll - bone.roll
        