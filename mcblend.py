import bpy
import mathutils
import struct

def write_some_data(context, filepath):
    print("Running BlendMC exporter...")
    f = open(filepath, 'w')
    scn = bpy.context.scene
    curFrame = scn.frame_current
    obj = scn.camera
    action = obj.animation_data.action
    f.write("BLENDMC\n")
    f.write(str(scn.frame_start) + "\n")
    f.write(str(scn.frame_end) + "\n")
    f.write(str((scn.frame_end - scn.frame_start)) + "\n")
    for frame in range(scn.frame_start, scn.frame_end):
            scn.frame_set(frame)
            f.write(str(obj.location[0]) + "\n")
            f.write(str(obj.location[1]) + "\n")
            f.write(str(obj.location[2]) + "\n")
            f.write(str(obj.rotation_euler[0]) + "\n")
            f.write(str(obj.rotation_euler[1]) + "\n")
            f.write(str(obj.rotation_euler[2]) + "\n")
            obj = scn.camera # We reset it here in case the camera changes mid-playback
    scn.frame_set(curFrame)
    # Write Frame Markers
    f.write(str(len(scn.timeline_markers.values())) + "\n")
    for marker in scn.timeline_markers.values():
        f.write(str(marker.name) + "\n")
        f.write(str(marker.frame) + "\n")
    f.close()
    return {'FINISHED'}

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

class ExportSomeData(Operator, ExportHelper):
    """Exports BlendMC Camera data"""
    bl_idname = "export_test.some_data"
    bl_label = "Export Some Data"

    filename_ext = ".blendmc"

    filter_glob: StringProperty(
        default="*.blendmc",
        options={'HIDDEN'},
        maxlen=255,
    )


    def execute(self, context):
        return write_some_data(context, self.filepath)


def menu_func_export(self, context):
    self.layout.operator(ExportSomeData.bl_idname, text="BlendMC Camera Exporter")


def register():
    bpy.utils.register_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_class(ExportSomeData)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)


if __name__ == "__main__":
    register()

    bpy.ops.export_test.some_data('INVOKE_DEFAULT')
