import bpy
import mathutils


def changeLocation(obj, x, y, z):
    obj.location = mathutils.Vector((x, y, z))


if __name__ == '__main__':
    activeObj = bpy.context.active_object
    changeLocation(activeObj, 2, 1, 0)
