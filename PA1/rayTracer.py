#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image 

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma;
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)

class Shader:
    def __init__(self, type, name, diffuse):
        self.type = type
        self.name = name
        self.diffuseColor = diffuse

class Lambertian(Shader):
    def __init__(self, type, name, diffuse):
        super().__init__(type, name, diffuse)

class Phong(Shader):
    def __init__(self, type, name, diffuse, specular, exponent):
        super().__init__(type, name, diffuse)
        self.specularColor = specular
        self.exponent = exponent

class SphereObj:
    def __init__(self, type, shader_ref, center, radius):
        self.type = type
        self.shader_ref = shader_ref
        self.center = center
        self.radius = radius

class Camera:
    def __init__(self, viewPoint, viewDir, viewUp, viewProjNormal, projDistance, viewWidth, viewHeight):
        self.viewPoint = viewPoint
        self.viewDir = viewDir
        self.viewUp = viewUp
        self.viewProjNoraml = viewProjNormal
        self.projDistance = projDistance
        self.viewWidth = viewWidth
        self.viewHeight = viewHeight

class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

class Ray:
    def __init__(self, start_pos, direction):
        self.start_pos = start_pos
        self.direction = direction

def find_solution_t(b, D, object):
    if D >= 0:
        t_zero = -b + np.sqrt(D)
        t_one = -b - np.sqrt(D)

        # negative t cannot exist
        if t_zero > 0 and t_one > 0:
            return object, min(t_zero, t_one)
        elif t_zero > 0:
            return object, t_zero
        elif t_one > 0:
            return object, t_one
        
    return None, None

def ray_intersect(ray, object):
    if object.type == 'Sphere':
        p = ray.start_pos - object.center
        b = np.dot(p, ray.direction)
        c = np.dot(p, p) - object.radius**2
        D = b**2 - c
        
        return find_solution_t(b, D, object)

def first_ray_intersect(ray, objects):
    tBest = np.inf
    firstSurface = None
    for object in objects:
        hitSurface, t = ray_intersect(ray, object)
        if hitSurface and t < tBest:
            tBest = t
            firstSurface = hitSurface
    
    return firstSurface, tBest

def light_intersect(object, first_intersection, light_source):
    if object.type == 'Sphere':
        light_dir = first_intersection - light_source.position
        light_dir_unit = light_dir / np.linalg.norm(light_dir)
        p = light_source.position - object.center
        b = np.dot(p, light_dir_unit)
        c = np.dot(p, p) - object.radius**2
        D = b**2 - c

        return find_solution_t(b, D, object)


def first_light_intersect(objects, first_intersection, light_source):
    tBest = np.inf
    first_light_surface = None
    for object in objects:
        hit_light_surface,t = light_intersect(object, first_intersection, light_source)
        if hit_light_surface and t < tBest:
            first_light_surface = hit_light_surface
            tBest = t

    return first_light_surface
    
def check_shadow(objects, firstSurface, first_intersection, light_source):
    first_light_surface = first_light_intersect(objects, first_intersection, light_source)

    # return True if other object is closer to the light, else return False
    if firstSurface == first_light_surface:
        return False
    else:
        return True
    
def Lambertian_shading(l, n, shader, light_source):
    diffuseColor = shader.diffuseColor
    r = diffuseColor[0] * light_source.intensity[0] * max(0, np.dot(n, l))
    g = diffuseColor[1] * light_source.intensity[1] * max(0, np.dot(n, l))
    b = diffuseColor[2] * light_source.intensity[2] * max(0, np.dot(n, l))

    return r, g, b

def Specular_shading(h, n, shader, light_source):
    specularColor = shader.specularColor
    r = specularColor[0] * light_source.intensity[0] * pow(max(0,np.dot(n, h)), shader.exponent)
    g = specularColor[1] * light_source.intensity[1] * pow(max(0,np.dot(n, h)), shader.exponent)
    b = specularColor[2] * light_source.intensity[2] * pow(max(0,np.dot(n, h)), shader.exponent)

    return r, g, b
    
    
def shading(firstSurface, first_intersection, ray, light_source):
    l = light_source.position - first_intersection
    l_unit = l / np.linalg.norm(l)
    n = first_intersection - firstSurface.center
    n_unit = n / np.linalg.norm(n)
    v = -1 * ray.direction
    v_unit = v / np.linalg.norm(v)

    shader = firstSurface.shader_ref
    if shader.type == 'Phong':
        h = v_unit + l_unit
        h_unit = h / np.linalg.norm(h)
        
        r1, g1, b1 = Lambertian_shading(l_unit, n_unit, shader, light_source)
        r2, g2, b2 = Specular_shading(h_unit, n_unit, shader, light_source)

        return r1+r2, g1+g2, b1+b2
    
    elif shader.type == 'Lambertian':
        return Lambertian_shading(l_unit, n_unit, shader, light_source)
        

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()
    # save shader objects
    shaders = []
    # save drawing objects
    objects = []

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64)
    viewUp=np.array([0,1,0]).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.

    # set camera values
    for c in root.findall('camera'):
        viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float64)
        viewDir=np.array(c.findtext('viewDir').split()).astype(np.float64)
        viewUp=np.array(c.findtext('viewUp').split()).astype(np.float64)
        viewProjNormal=-1*viewDir
        if c.findtext('projDistance'):
            projDistance=float(c.findtext('projDistance'))
        viewWidth=float(c.findtext('viewWidth'))
        viewHeight=float(c.findtext('viewHeight'))

    camera = Camera(viewPoint, viewDir, viewUp, viewProjNormal, projDistance, viewWidth, viewHeight)

    # set shader values
    for c in root.findall('shader'):
        type_name = c.get('type')
        shader_name = c.get('name')
        diffuseColor=np.array(c.findtext('diffuseColor').split()).astype(np.float64)
        if type_name == "Lambertian":
            shaders.append(Lambertian(type_name, shader_name, diffuseColor))
        elif type_name == "Phong":
            specularColor = np.array(c.findtext('specularColor').split()).astype(np.float64)
            exponent = float(c.findtext('exponent'))
            shaders.append(Phong(type_name, shader_name, diffuseColor, specularColor, exponent))

    # set sphere values
    for c in root.findall('surface'):
        type_name = c.get('type')
        if type_name == "Sphere":
            for shader in shaders:
                if c.find('shader').get('ref') == shader.name:
                    shader_ref = shader
                    break
            center = np.array(c.findtext('center').split()).astype(np.float64)
            radius = float(c.findtext('radius'))
            objects.append(SphereObj(type_name, shader_ref, center, radius))
    
    # set light values
    for c in root.findall('light'):
        light_pos = np.array(c.findtext("position").split()).astype(np.float64)
        light_intensity = np.array(c.findtext('intensity').split()).astype(np.float64)
    
    light_source = Light(light_pos, light_intensity)

    # Create an empty image
    imgSize=np.array(root.findtext('image').split()).astype(np.int32)
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # define u, v vectors for pixel-to-image mapping
    w = camera.viewDir
    u = np.cross(w, camera.viewUp)
    v = np.cross(w, u)
    w_unit = w / np.linalg.norm(w)
    u_unit = u / np.linalg.norm(u)
    v_unit = v / np.linalg.norm(v)
    # pdb.set_trace()
    img_center = camera.viewPoint + (w_unit * camera.projDistance)
    img_start = img_center - (u_unit * camera.viewWidth / 2) - (v_unit * camera.viewHeight / 2)

    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            pixel_coords = img_start + (u_unit * (x + 0.5) * camera.viewWidth / imgSize[0]) + (v_unit * (y + 0.5) * camera.viewHeight / imgSize[1])
            ray_dir = pixel_coords - camera.viewPoint
            ray_dir_unit = ray_dir / np.linalg.norm(ray_dir)
            ray = Ray(camera.viewPoint, ray_dir_unit)
            firstSurface, t = first_ray_intersect(ray, objects)
            if firstSurface == None:
                continue
            first_intersection = ray.start_pos + (ray_dir_unit * t)
            check = check_shadow(objects, firstSurface, first_intersection, light_source)
            if not check:
                r, g, b = shading(firstSurface, first_intersection, ray, light_source)
                pixel_color = Color(r, g, b)
                pixel_color.gammaCorrect(2.2)
                img[y][x] = pixel_color.toUINT8()

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()
