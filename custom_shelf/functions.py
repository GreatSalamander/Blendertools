import bpy
import os
import glob
from bpy.props import PointerProperty

def read_shelves() :
    shelves = bpy.context.scene.CustomShelf.folders
    path = os.path.join(os.path.dirname(__file__),'shelves')
    #shelves = {}

    scripts = glob.glob(path+'/*/*.py')
    folders = os.listdir(path)


    for s in scripts :
        folder_name = os.path.basename(os.path.dirname(s))
        script_name = os.path.splitext(os.path.basename(s))[0]

        if script_name!='__init__' :
            text= open(s)
            lines=text.readlines()
            icon='FILE_TEXT'
            description = ''

            if len(lines)>1 and lines[0].startswith('icon'):
                icon=eval(lines[0].split('=')[1])

            elif len(lines)>2 and lines[1].startswith('description'):
                description=eval(lines[1].split('=')[1])

            if not shelves.get(folder_name) :
                shelves[folder_name] = {'scripts':{},'expand':True}

            shelves[folder_name]['scripts'][script_name]= {'icon':icon,'description':description,'path':folder_name+'/'+script_name}

    #return(shelves)
