import bpy
import os
from .functions import read_shelves

class CustomShelfVariables(bpy.types.PropertyGroup) :
    pass

class CustomShelfFolders(bpy.types.PropertyGroup) :
    pass

class CustomShelfSettings(bpy.types.PropertyGroup) :
    folders = bpy.props.PointerProperty(type= CustomShelfFolders)
    variables = bpy.props.PointerProperty(type= CustomShelfVariables)
class CustomShelfPanel(bpy.types.Panel):
    bl_label = "Custom Shelf"
    bl_category = "SHELFS"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    # bl_context = "posemode"

    def draw_header(self, context):
        view = context.space_data
        layout = self.layout
        row=layout.row(align=True)
        row.operator("customshelf.refresh",text='',emboss=False,icon= "FILE_REFRESH")

    def draw(self, context):
        layout = self.layout

        window = context.window
        scene = context.scene
        rd = scene.render

        shelves = bpy.context.scene.CustomShelf.folders

        col = layout.column(align=False)
        for key,value in sorted(shelves.items()) :
            box = col.box()
            box.alignment='EXPAND'

            if value['expand'] == True :
                expandIcon = 'TRIA_DOWN'
            else :
                expandIcon = 'TRIA_RIGHT'

            row = col.row(align = True)
            #row.alignment = 'CENTER'
            row.operator("customshelf.expand",text='',icon = expandIcon,emboss=False).folder = key
            row.label(key.upper())

            #col.separator()
            if value['expand'] == True :

                #text =' '.join([' ' for a in range(0,len(key))])
                #row.prop(context.scene.CustomShelf,key,emboss = False,text=' ')


                for script,settings in sorted(value['scripts'].items()) :
                    #print(s[1])
                    func = col.operator("customshelf.run_function",text=script,icon = settings['icon'])
                    func.path = settings['path']

                col.separator()
                col.separator()



class CustomShelfPrefs(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    globalpath = os.path.join(os.path.dirname(os.path.dirname(__file__)),'shelves')

    localShelf = bpy.props.StringProperty(name="Local path",subtype = 'FILE_PATH')
    globalShelf = bpy.props.StringProperty(name="Global path",subtype = 'FILE_PATH',default =globalpath )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "localShelf")
        layout.prop(self, "globalShelf")
