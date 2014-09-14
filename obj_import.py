import world
import color
import os
from os import path
from mesh import *
from geometry import Vec3
from materials import BSDF
from world import World

class ObjMaterial:
    """ an Wavefront Object material specification """
    def __init__(self, name):
        self.diffuse = color.Color((0, 0, 0))
        self.specular = color.Color((0, 0, 0))
        self.name = name

    def __str__(self):
        return "<ObjMaterial: {name} {diffuse} {specular}>".format(**self.__dict__)

    def __repr__(self):
        return "<ObjMaterial: {name} {diffuse} {specular}>".format(**self.__dict__)

class ObjObject:
    def __init__(self, name):
        self.name = name;
        self.faces = []

class ObjTransient:
    """ misc. data used when importing obj. files """
    def __init__(self):
        self.materials = {}
        self.verts = []
        self.normals = []
        self.faces = []
        self.objects = {}

def read_three_floats(line):
    return [float(x) for x in line[1:4]]

def parse_mtllib(data, fname):
    print('parsing mtllib', fname)
    parsing = None
    with open(fname) as f:
        for line in f:
            line = line.lower()
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                continue
            line = line.split()
            if line[0] == 'newmtl':
                parsing = ObjMaterial(' '.join(line[1:]))
                data.materials[parsing.name] = parsing
            elif line[0][0] == 'k':
                col = color.Color(read_three_floats(line))
                if line[0][1] == 'd':
                    parsing.diffuse = col
                elif line[0][1] == 's':
                    parsing.specular = col
    data.materials[parsing.name] = parsing

def parse_obj_vertex(data, v):
    v = v.split('/')
    pos = data.verts[int(v[0]) - 1]
    normal = data.normals[int(v[2]) - 1]
    return Vertex(pos, normal)

def create_real_material(mat):
    return BSDF(mat.diffuse)

def load(fname_base):
    folder = path.dirname(path.abspath(fname_base))
    base_name = path.abspath(fname_base)
    data = ObjTransient()
    parsing_object = None
    current_material = None
    with open(base_name + '.obj') as base_file:
        for line in base_file:
            line = line.strip().split(' ')
            if line[0] == '#':
                continue
            elif line[0] == 'mtllib':
                parse_mtllib(data, path.join(folder,' '.join(line[1:])))
            elif line[0] == 'v':
                data.verts.append(Vec3(*read_three_floats(line)))
            elif line[0] == 'vn':
                data.normals.append(Vec3(*read_three_floats(line)))
            elif line[0] == 'o':
                base_obj_name = ' '.join(line[1:])
                obj_name = base_obj_name + '.0'
                i = 0
                while obj_name in data.objects:
                    obj_name = base_obj_name + '.{0}'.format(i)
                    i += 1
                data.objects[obj_name] = ObjObject(obj_name)
                parsing_object = data.objects[obj_name]
            elif line[0] == 'usemtl':
                current_material = data.materials[' '.join(line[1:]).lower()]
            elif line[0] == 'f':
                a = parse_obj_vertex(data, line[1])
                b = parse_obj_vertex(data, line[2])
                c = parse_obj_vertex(data, line[3])
                tri = Triangle(a, b, c, create_real_material(current_material))
                data.faces.append(tri)

    print("Read {vcount} verts and {ncount} normals, which formed {fcount} faces".format(vcount=len(data.verts), ncount=len(data.normals), fcount=len(data.faces)))
    return World(data.faces)

if __name__ == '__main__':
    import sys
    load(sys.argv[1])
