bl_info = {
    "name": "Animation Tweaks",
    "author": "Christophe Seux, Manuel Rais",
    "version": (0, 1),
    "blender": (2, 77, 0),
    "location": "",
    "description": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Animation"}

if "bpy" in locals():
    import imp
    imp.reload(operators)
    imp.reload(panels)

else:
    from . import operators
    from . import panels

import bpy

addon_keymaps = []
def register():
    bpy.utils.register_module(__name__)

    addon = bpy.context.window_manager.keyconfigs.addon
    if addon:
        km = addon.keymaps.new(name = "3D View", space_type = "VIEW_3D")
        km.keymap_items.new("pose.insert_keyframe", type = "K", value = "PRESS")
        km.keymap_items.new("pose.reset_props", type = "X", value = "PRESS")
        addon_keymaps.append(km)


def unregister():
    bpy.utils.unregister_module(__name__)

    wm = bpy.context.window_manager
    for km in addon_keymaps:
        for kmi in km.keymap_items:
            km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()
