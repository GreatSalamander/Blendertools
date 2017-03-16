import bpy
import os
import sys
import importlib
from .panels import CustomShelfVariables,CustomShelfSettings
from .functions import read_shelves

class CustomShelfRefresh(bpy.types.Operator):
    bl_idname = "customshelf.refresh"
    bl_label = 'Refresh Shelves'

    def execute(self,context) :
        read_shelves()

        return {'FINISHED'}

class CustomShelfRunFunction(bpy.types.Operator):
    bl_idname = "customshelf.run_function"
    bl_label = 'Run Function'

    #variables = {}
    path = bpy.props.StringProperty()
    #folder = bpy.props.StringProperty()
    #variables = bpy.props.PointerProperty(type = bpy.types.PropertyGroup)

    Types={
    str : bpy.props.StringProperty,
    int : bpy.props.IntProperty,
    float : bpy.props.FloatProperty,
    #list : bpy.props.StringProperty,
    }

    def execute(self,context) :
        folder = os.path.dirname(self.path)
        script = os.path.basename(self.path)
        exec('from .shelves.%s import %s'%(folder,script))
        importlib.reload(eval(script))


        variables={}
        for v in self.variables :
            variables[os.path.basename(v)] = context.scene.CustomShelf.variables['%s/%s/%s'%(folder,script,v)]

        exec('%s.main(%s)'%(script,variables))

        return {'FINISHED'}


    def invoke(self, context, event):
        shelves = bpy.context.scene.CustomShelf.folders
        folder = os.path.dirname(self.path)
        script = os.path.basename(self.path)

        self.bl_label = script.title()
        exec('from .shelves.%s import %s'%(folder,script))
        importlib.reload(eval(script))

        #print(eval('%s.variables'%self.script))
        self.variables = eval('%s.variables'%script)

        #for key,value in context.scene.CustomShelfVars.items() :

        for key,value in self.variables.items()  :
            if type(value) in self.Types :
                Type  = self.Types[type(value)]
                if type(value)== list:
                    value = str(value)

                setattr(CustomShelfVariables,'%s/%s/%s'%(folder,script,key), Type(default = value))
                setattr(context.scene.CustomShelf.variables,'%s/%s/%s'%(folder,script,key),value)


        #context.scene.CustomShelfVars.a='toto'

        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        folder = os.path.dirname(self.path)
        script = os.path.basename(self.path)

        col = layout.column(align=False)
        for key,value in sorted(self.variables.items()) :



            if type(value) in self.Types :
                col.prop(context.scene.CustomShelf.variables, '%s/%s/%s'%(folder,script,key), expand=False,toggle=True,text=key)
            '''
            else :
                Type = str([value])[1:-1].replace("bpy.data.","").split('[')[0]#getting the data adress e.g bpy.data.objects

                data_path

                print(Type)
                #col.prop(context.scene.CustomShelf.variables, key, expand=True,text = key)
                col.prop_search(context.scene.CustomShelf.variables, key, data_path,Type,text = key)
                #col.prop_search(context.scene.CustomShelf.variables, key, bpy.data.objects['Armature'].pose,'bones',text = key)
            '''

class CustomShelfExpand(bpy.types.Operator):
    bl_idname = "customshelf.expand"
    bl_label = "Expand shelf"

    folder = bpy.props.StringProperty()

    def execute(self, context):
        folder = self.folder
        shelves = bpy.context.scene.CustomShelf.folders

        shelves[folder]['expand'] = not shelves[folder]['expand']


        return {'FINISHED'}
