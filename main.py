import obj_import
from geometry import Vec3
from sys import argv

world = obj_import.load(argv[1])

world.kvtree.render_debug_wavefront_mesh('test.obj')

world.trace_ray(Vec3(0, 2, 0), Vec3(0.1, -1, 0.1))
