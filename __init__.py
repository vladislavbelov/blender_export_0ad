bl_info = {
    "name": "0 A.D. Export",
    "author": "Vladislav Belov",
    "version": (0, 0, 22),
    "blender": (2, 75, 0),
    "location": "0 A.D. Exporter Menu",
    "description": "Allow export objects to 0 A.D. actors",
    "wiki_url": "https://github.com/vladislavbelov/blender_export_0ad/wiki",
    "tracker_url": "https://github.com/vladislavbelov/blender_export_0ad/issues",
    "category": "Import-Export"
}


# Reload modules
if "bpy" in locals():
    import importlib
    if "export_0ad" in locals():
        importlib.reload(export_0ad)


# External modules
import bpy
import bpy.utils.previews
import bpy.props
import os


# Internal modules
from . import export_0ad


class View3DPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "0 A.D. Export"
    bl_options = {"DEFAULT_CLOSED"}


class ExportSettingsPanel(View3DPanel):
    bl_label = "Export Settings"
    bl_options = {"HIDE_HEADER"}

    def draw(self, context):
        column = self.layout.column(align=True)
        column.prop(context.scene, "public_mod_path")
        column.separator()
        column.prop(context.scene, "mod_path")
        column.separator()


class ExportActorPanel(View3DPanel):
    bl_label = "Export Actor"

    def draw(self, context):
        column = self.layout.column(align=True)
        column.operator(
            "export0ad.actor",
            text="Export to 0 A.D.",
            icon_value=addon_icons["0ad"].icon_id)
        column.separator()


class ExportEntityPanel(View3DPanel):
    bl_label = "Export Entity"

    def draw(self, context):
        self.layout.label("Not implemented yet", icon="ERROR")
        column = self.layout.column(align=True)
        column.separator()


def get_addon_classes():
    addon_classes = [
        ExportSettingsPanel,
        ExportActorPanel,
        ExportEntityPanel,
    ]
    addon_classes += export_0ad.get_classes_to_register()
    return addon_classes


def register_icons():
    global addon_icons
    addon_icons = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    addon_icons.load("0ad", os.path.join(icons_dir, "0ad.png"), "IMAGE")


def unregister_icons():
    global addon_icons
    bpy.utils.previews.remove(addon_icons)


def update_public_mod_path(self, context):
    # Public Mod Path should be valid and contain resources folders or public.zip
    if not export_0ad.is_valid_public_mod_directory(self["public_mod_path"]):
        # TODO: add an error message
        self["public_mod_path"] = ""


def update_mod_path(self, context):
    # Public Mod Path should be valid and contain resources folders or public.zip
    if not os.path.isdir(self["mod_path"]):
        # TODO: add an error message
        self["mod_path"] = ""


def register():
    register_icons()
    for cls in get_addon_classes():
        bpy.utils.register_class(cls)

    default_0ad_path = ""
    bpy.types.Scene.public_mod_path = bpy.props.StringProperty(
        name="Public Mod Path",
        default=default_0ad_path,
        description="A path to the public 0 A.D. mod, which contains all basic resources (textures, materials, etc).",
        subtype="DIR_PATH",
        update=update_public_mod_path
    )
    bpy.types.Scene.mod_path = bpy.props.StringProperty(
        name="Mod Path",
        default=default_0ad_path,
        description="Define a path to any 0 A.D. mod (public or your own)",
        subtype="DIR_PATH",
        update=update_mod_path
    )


def unregister():
    unregister_icons()
    for cls in get_addon_classes():
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.public_mod_path
    del bpy.types.Scene.mod_path


if __name__ == "__main__":
    register()
