import blenderproc as bproc
import blenderproc.python.types.MeshObjectUtility
import numpy as np


def init_objects(object_names: [], mesh_objects: []):
    mesh_objects = [m for m in mesh_objects if isinstance(m, blenderproc.types.MeshObject)]
    print(len(object_names))
    print(len(mesh_objects))
    print(mesh_objects[0].get_name())
    return [bproc.filter.one_by_attr(mesh_objects, "name", f"{o}.*", regex=True) for o in object_names]


def hide_object(mesh_objects: [blenderproc.types.MeshObject]):
    for mesh_object in mesh_objects:
        mesh_object.blender_obj.hide_render = True


def get_cam_poses(locations: [float], poi: [float]):
    for location in locations:
        # Sample random camera location above objects
        # location = np.random.uniform([3.1, -2.4, 1.0], [3.5, -2.5, 1.4])
        location = location
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - np.array(location),
                                                                 inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)


def set_rendering_of_object(blender_objects, render):
    for b_object in blender_objects:
        b_object.blender_obj.hide_render = False


def set_random_rotation_zaxis(blender_objects):
    for b_object in blender_objects:
        rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
        b_object.set_rotation_euler(b_object.get_rotation_euler() + rotation)


def set_homogeneous_lighting(locations, strength: float):
    for location in locations:
        light = bproc.types.Light()
        light.set_location(location)
        light.set_energy(strength)
