bl_info = {
    "name": "UI tweak",
    "author": "Christophe Seux",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "category": "User"}


import bpy
import os
from bpy.app.handlers import persistent

oldPreset = {}

def read_preset():
    preset = {}

    addon_prefs = bpy.context.user_preferences.addons[__name__].preferences.presets
    presetFolder = os.path.join(os.path.dirname(__file__),'presets')


    pyFile = os.path.join(presetFolder,addon_prefs+'.py')

    with open(pyFile,'r') as text:
        for line in text:
            key = line.split('=')[0]
            value = line.split(';')[0].split('=')[1]
            preset[key] = [v for v in value.split(',')]

    return (preset)


#preset = read_preset()[0]

def read_presetList() :
    presetFolder = os.path.join(os.path.dirname(__file__),'presets')
    presetName = [os.path.splitext(p)[0] for p in os.listdir(presetFolder)]

    return(presetName)

def update(self,context):
    apply_UI(True,True)
    print(oldPreset)

def apply_UI(register,unregister):

    preset = read_preset()

    if oldPreset and unregister == True:
        for pt in bpy.types.Panel.__subclasses__():
            if pt.bl_space_type == 'VIEW_3D' and pt.bl_label in oldPreset['panelToRemove']:
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.register_class(pt)

            elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in oldPreset['panelToDisplay']:
                for panel in oldPreset['panelToDisplay'] :
                    if "bl_rna" in pt.__dict__:
                        bpy.utils.unregister_class(pt)

                    pt.bl_region_type = 'UI'
                    bpy.utils.register_class(pt)

            elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in oldPreset['panelToView']:
                for panel in oldPreset['panelToView'] :
                    if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                        bpy.utils.unregister_class(pt)

                    pt.bl_region_type = 'UI'
                    bpy.utils.register_class(pt)

    if register == True :
        for pt in bpy.types.Panel.__subclasses__():
            if pt.bl_space_type == 'VIEW_3D' and pt.bl_label in preset['panelToRemove']:
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.unregister_class(pt)

            elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in preset['panelToDisplay']:
                for panel in preset['panelToDisplay'] :
                    if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                        bpy.utils.unregister_class(pt)

                    pt.bl_category = "Display"
                    #pt.bl_space_type = 'VIEW_3D'
                    pt.bl_region_type = 'TOOLS'

                    bpy.utils.register_class(pt)

            elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in preset['panelToView']:
                for panel in preset['panelToView'] :
                    if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                        bpy.utils.unregister_class(pt)

                    pt.bl_category = "View"
                    #pt.bl_space_type = 'VIEW_3D'
                    pt.bl_region_type = 'TOOLS'

                bpy.utils.register_class(pt)

    oldPreset['panelToRemove'] = preset['panelToRemove']
    oldPreset['panelToDisplay'] = preset['panelToDisplay']
    oldPreset['panelToView'] = preset['panelToView']

class UiTweakPrefs(bpy.types.AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    items =[]
    for p in read_presetList():
        items.append(p)

    itemsSort =[]
    for p in sorted(items):
        itemsSort.append((p,p,""))

    presets = bpy.props.EnumProperty(name="Presets",items=itemsSort,description="Shape",update = update)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "presets")



@persistent
def apply_UI_handler(dummy):
    apply_UI(True,True)




def register():
    bpy.utils.register_class(UiTweakPrefs)
    bpy.app.handlers.load_post.append(apply_UI_handler)


def unregister():
    apply_UI(False,True)
    bpy.utils.unregister_class(UiTweakPrefs)
    bpy.app.handlers.load_post.remove(apply_UI_handler)


    '''
    for pt in bpy.types.Panel.__subclasses__():
        if pt.bl_space_type == 'VIEW_3D' and pt.bl_label in panelToRemove:
            if not "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                bpy.utils.register_class(pt)


        elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in panelToDisplay+panelToView:
            for panel in panelToDisplay :
                pt.bl_category = "Display"
                pt.bl_space_type = 'VIEW_3D'
                pt.bl_region_type = 'UI'

                if not "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.register_class(pt)
    '''
