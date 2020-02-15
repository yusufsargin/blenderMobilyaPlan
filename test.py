def transformObj(radiand=270, direction='Z'):
    """
    The Object to transform, should selected before use this function.
    import mathutils,import bpy and import math should add for stable work.
    """

    switcher = {
        'X': mathutils.Euler((math.radians(radiand), 0, 0), 'XYZ')[0],
        'Y': mathutils.Euler((0, math.radians(radiand), 0), 'XYZ')[1],
        'Z': mathutils.Euler((0, 0, math.radians(radiand)), 'XYZ')[2],
    }

    """
    @return {'FINISHED'} 
    """
    return bpy.ops.transform.rotate(value=switcher.get(direction, 'Z'), orient_axis='Z',
                                    orient_type='GLOBAL',
                                    orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL',
                                    constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False,
                                    proportional_edit_falloff='SMOOTH', proportional_size=1,
                                    use_proportional_connected=False,
                                    use_proportional_projected=False);
