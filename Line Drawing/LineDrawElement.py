import bpy


class LineOperation:
    def __init__(self, coordinate=[(0, 0, 0), (0, 0, 0), (0, 0, 0)]):
        self.coordinate = coordinate

    def createNewCurveObj(self, name='test'):
        bpy.data.curves.new(name, 'CURVE')

    def meshLinkToScene(self, mesh, name):
        obj = bpy.data.objects.new(name, mesh)
        bpy.context.scene.objects.link(obj)


if '__name__' == '__main__':
    test = LineOperation()
