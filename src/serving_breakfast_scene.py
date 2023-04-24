import blenderproc as bproc
import numpy as np
import os
import shutil
import json
import random
import sys
sys.path.append("/home/sorin/code/blenderproc/src")
import utils

bproc.init()
object_list = []
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
# Create a simple object:
#objs = bproc.loader.load_obj("/home/sorin/data/blenderproc/data/saved_scenes/objects_on_table_final_18_objects.obj")
objs = bproc.loader.load_blend("/home/sorin/data/blenderproc/data/saved_scenes/serving_breakfast.blend")
output_path="/home/sorin/code/blenderproc/output"
shutil.rmtree(output_path + "/coco_data")

for j, obj in enumerate(objs):
    obj_list = utils.create_list_from_id2json()
    print(obj.get_name())
    if obj.get_name() in obj_list:
        obj_id = utils.get_id_of_object(obj.get_name())
        obj.set_cp("category_id", obj_id)
    else:
        obj.set_cp("category_id", j + 10000)

# Initialization of perceiving objects
furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)
# Definition of the objects in the scene from bottom left of the table to top right (as seen from z)
# first objects
milk = bproc.filter.one_by_attr(objs, "name", "MilkPack")
bowl = bproc.filter.one_by_attr(objs, "name", "Bowl")
cereal = bproc.filter.one_by_attr(objs, "name", "CerealBox")
spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")

first_pos = [4.7, -2.27, 0]
second_pos = [4.7, -2.43, 0]
third_pos = [4.7, -2.64, 0]
fourth_pos = [4.7, -2.86, 0]
pos_list = [first_pos, second_pos, third_pos, fourth_pos]
serving_breakfast = [milk, bowl, cereal, spoon]

# Create a point light next to it
def room_light(strength):
    light = bproc.types.Light()
    light2 = bproc.types.Light()
    light3 = bproc.types.Light()
    light4 = bproc.types.Light()
    light5 = bproc.types.Light()
    light6 = bproc.types.Light()
    light7 = bproc.types.Light()
    light8 = bproc.types.Light()
    light.set_location([2, -2, 2])
    light2.set_location([3, -2, 2])
    light3.set_location([4, -2, 2])
    light4.set_location([5, -2, 2])
    light5.set_location([2, -3, 2])
    light6.set_location([3, -3, 2])
    light7.set_location([4, -3, 2])
    light8.set_location([5, -3, 2])
    light.set_energy(strength)
    light2.set_energy(strength)
    light3.set_energy(strength)
    light4.set_energy(strength)
    light5.set_energy(strength)
    light6.set_energy(strength)
    light7.set_energy(strength)
    light8.set_energy(strength)

room_light(100)


# Find point of interest, all cam poses should look towards it
#poi = bproc.object.compute_poi(objs)
poi = [4.7, -2.6, 0.8]
bproc.camera.set_resolution(640, 480)
print(poi)
#rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
def hide():
    for item in object_list:
        item.blender_obj.hide_render = True

def camer_poses(x):
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([3.1, -2.3, 1], [3.3, -2.9, 1.4])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)


def swap_location(obj_to_be_moved, new):
    obj_z = obj_to_be_moved.get_location()[2]
    new_location = [new[0], new[1], obj_z]
    obj_to_be_moved.set_location(new_location)


def deploy_scene(x):
    for i in range(x):

        random.shuffle(pos_list)
        random.shuffle(serving_breakfast)

        new_list = zip(serving_breakfast, pos_list)

        for item in new_list:
            swap_location(item[0], item[1])

        for item in serving_breakfast:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            x_mov = np.random.uniform([4.6], [4.9])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)
            item.set_location([x_mov, item.get_location()[1], item.get_location()[2]])

        for obj in furnitures:
            obj.blender_obj.hide_render = False

            # Render the scene
        data = bproc.renderer.render()
            # Write the rendering into an hdf5 file

        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join(output_path, 'coco_data'),
                                                    instance_segmaps=seg_data["instance_segmaps"],
                                                    instance_attribute_maps=seg_data["instance_attribute_maps"],
                                                    colors=data["colors"],
                                                    color_file_format="JPEG")
        bproc.writer.write_hdf5(output_path, data)

def pipeline():
    camer_poses(5)
    deploy_scene(10)


pipeline()