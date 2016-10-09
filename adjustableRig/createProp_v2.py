import bpy
from mathutils import Vector,Matrix
from math import sqrt
import numpy

MASTER_bones = []
SCALE_bones = []
armature = bpy.context.active_object.data

def zero_issue(Vect):
    for i in range(0,3):
        if -numpy.finfo(numpy.float).eps*1e10 <= abs(Vect[i]) <= numpy.finfo(numpy.float).eps*1e10:
            Vect[i] = numpy.finfo(numpy.float).eps
    return(Vect)

def between(a,b,c,Inside=False):
    
    C = bpy.context
    D = bpy.data
    
    '''
    print(a,c)
    print(a==c)
    print(b,c)
    print(b==c)
    '''
    
    a=zero_issue(a)
    b=zero_issue(b)
    c=zero_issue(c)
    
    if not Inside:
        if ( round((b-a).cross(c-a).length,4) == 0.0 and (  0 <= (b-a).dot(c-a) <= numpy.linalg.norm(a-b)**2 ) ) or a==c or b==c:
            return round(1- c.cross(b).length / a.cross(b).length,5)
        else:
            return(False)
    if Inside:
        if round((b-a).cross(c-a).length,4) == 0.0:
            return round(1- c.cross(b).length / a.cross(b).length,5)
        else:
            return(False)


for bone in bpy.context.active_object.data.edit_bones :
#for bone in bpy.context.selected_editable_bones :
    if bone.name.startswith("REF-") :
        
        MASTER_bones.append(bone)
        
    else :
        
        SCALE_bones.append(bone)
        

for bone in SCALE_bones :
    customProp = ["head","headParent","tail","tailParent","roll"]
    
    for prop in customProp :
        try:
            del(bone[prop])

        except KeyError:
            pass

    for masterBone in MASTER_bones :
        #print(bone.name)
        #print(masterBone.name)
        a = Vector(masterBone.head)
        b = Vector(masterBone.tail)
        c = Vector(bone.head)
        d = Vector(bone.tail)
        
        
        #print(bone.name)
        print(masterBone.name)      
        bHead = between(a,b,c)
        bTail = between(a,b,d)

        
        if type(bHead)!= type(False):
            bone["head"] = bHead
            bone["headParent"]= masterBone.name
            bone["roll"]= round(masterBone.roll - bone.roll,4)   
           
        if type(bTail)!= type(False):
            bone["tail"] = bTail
            bone["tailParent"]= masterBone.name
            #bone["roll"]= masterBone.roll - bone.roll


for bone in SCALE_bones:
    if bone.get('tail')==None and bone.get('head')!=None:
        masterBone = bpy.context.active_object.data.edit_bones.get(bone['headParent'])
        bTail = between(masterBone.head,masterBone.tail,bone.tail,Inside=True)
        if type(bTail)!= type(False):
            bone["tail"] = bone["head"] + bone.length/masterBone.length
            bone["tailParent"]= masterBone.name
            bone["roll"]= masterBone.roll - bone.roll
    
    if bone.get('head')==None and bone.get('tail')!=None:
        masterBone = bpy.context.active_object.data.edit_bones.get(bone['tailParent'])
        bHead = between(masterBone.head,masterBone.tail,bone.head,Inside=True)
        if type(bHead)!= type(False):
            print(bone.length)
            bone["head"] = bone['tail'] + bone.length/masterBone.length
            bone["headParent"]= masterBone.name
            bone["roll"]= masterBone.roll - bone.roll

