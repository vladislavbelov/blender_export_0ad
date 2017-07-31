import bpy
import os
from bpy.props import StringProperty, BoolProperty, CollectionProperty, FloatProperty
from bpy_extras.io_utils import ExportHelper


def is_valid_public_mod_directory(path):
    if not os.path.isdir(path):
        return False
    required_subdirectories = ["art", "shaders", "simulation", "mod.json"]
    subdirectories = os.listdir(path)
    for subdir in required_subdirectories:
        if subdir not in subdirectories:
            return False
    return True


class ExportActor(bpy.types.Operator):
    """Save the active object to the 0 A.D. actor"""
    bl_idname = "export0ad.actor"
    bl_label = "Export 0 A.D."
    bl_category = "Export"

    def invoke(self, context, event):
        # TODO: implement export
        return {"FINISHED"}


# TODO: implement ExportEntity


def get_classes_to_register():
    return [
        ExportActor
    ]
