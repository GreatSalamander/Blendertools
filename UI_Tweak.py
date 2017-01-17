bl_info = {
    "name": "UI tweak",
    "author": "Christophe Seux",
    "version": (0, 1),
    "blender": (2, 78, 0),
    "category": "User"}



import bpy

panelToRemove=[
"Animation",
"Grease Pencil Layers",
"Item",
"Motion Tracking",
"Transform Orientations",
"Grease Pencil",
"Drawing Brushes",
"Rigid Body Tools",
"Relations",
"Add Primitive",
"Pose Options",

]

panelToDisplay =[
"Shading",
"Display",


]

panelToView =[
"View",
"Background Images",
"3D Cursor",

]


def register():
    for pt in bpy.types.Panel.__subclasses__():
        if pt.bl_space_type == 'VIEW_3D' and pt.bl_label in panelToRemove:
            if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                bpy.utils.unregister_class(pt)


        elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in panelToDisplay:
            for panel in panelToDisplay :
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.unregister_class(pt)

                pt.bl_category = "Display"
                pt.bl_space_type = 'VIEW_3D'
                pt.bl_region_type = 'TOOLS'

                bpy.utils.register_class(pt)

        elif pt.bl_space_type == 'VIEW_3D' and pt.bl_label in panelToView:
            for panel in panelToView :
                if "bl_rna" in pt.__dict__:   # <-- check if we already removed!
                    bpy.utils.unregister_class(pt)

                pt.bl_category = "View"
                pt.bl_space_type = 'VIEW_3D'
                pt.bl_region_type = 'TOOLS'

                bpy.utils.register_class(pt)


def unregister():
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
