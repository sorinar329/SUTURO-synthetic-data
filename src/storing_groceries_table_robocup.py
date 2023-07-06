import blenderproc as bproc
import numpy as np
import os
import shutil
import json
import random
import sys
sys.path.append("/home/suturo/Developer/blenderproc/SUTURO-synthetic-data/src")
import utils


bproc.init()
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
objs = bproc.loader.load_blend("/home/suturo/Developer/blender_data/robocup/scenes/robocup_table_serving_breakfast.blend")
output_path="/home/suturo/Developer/blenderproc/SUTURO-synthetic-data/robocuptable06_07"
#shutil.rmtree(output_path + "/coco_data")

objs_to_annotate = []

for j, obj in enumerate(objs):
    obj_list = utils.create_list_from_id2json()
    if "." in obj.get_name():
        if obj.get_name().split(".")[0] in obj_list:
            obj_id = utils.get_id_of_object(obj.get_name().split(".")[0])
            obj.set_cp("category_id", obj_id)

    elif obj.get_name() in obj_list:
        obj_id = utils.get_id_of_object(obj.get_name())
        obj.set_cp("category_id", obj_id)
    else:
        obj.set_cp("category_id", j + 10000)

#furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)


def init_objects():
    milk = bproc.filter.one_by_attr(objs, "name", "Milkbottle")
    milk1 = bproc.filter.one_by_attr(objs, "name", "Milkbottle.001")
    milk2 = bproc.filter.one_by_attr(objs, "name", "Milkbottle.002")
    cereal_box = bproc.filter.one_by_attr(objs, "name", "Cerealboxrobocup")
    cereal_box1 = bproc.filter.one_by_attr(objs, "name", "Cerealboxrobocup.001")
    cereal_box2 = bproc.filter.one_by_attr(objs, "name", "Cerealboxrobocup.002")
    cereal_box3 = bproc.filter.one_by_attr(objs, "name", "Cerealboxrobocup.003")
    cereal_box4 = bproc.filter.one_by_attr(objs, "name", "Cerealboxrobocup.004")
    cereal_box5 = bproc.filter.one_by_attr(objs, "name", "Cerealboxrobocup.005")
    bowl = bproc.filter.one_by_attr(objs, "name", "Bowl")
    bowl1 = bproc.filter.one_by_attr(objs, "name", "Bowl.001")
    bowl2 = bproc.filter.one_by_attr(objs, "name", "Bowl.002")
    spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")
    spoon1 = bproc.filter.one_by_attr(objs, "name", "Spoon.001")
    spoon2 = bproc.filter.one_by_attr(objs, "name", "Spoon.002")
    list_of_objects = [milk, milk1, milk2, cereal_box, cereal_box4, cereal_box3, cereal_box5, cereal_box2, cereal_box1,
                       bowl, bowl1, bowl2, spoon2, spoon, spoon1]

    return list_of_objects


lob = init_objects()


def positions():
    first_pos = [4.3, 5]
    second_pos = [4.3, 4.75]
    third_pos = [4.3, 4.5]
    fourth_pos = [4.3, 4.25]
    pos_list = [first_pos, second_pos, third_pos, fourth_pos]
    return pos_list


list_of_positions = positions()


def room_light(strength):
    # light = bproc.types.Light()
    # light2 = bproc.types.Light()
    light3 = bproc.types.Light()
    light4 = bproc.types.Light()
    # light5 = bproc.types.Light()
    # light6 = bproc.types.Light()
    light7 = bproc.types.Light()
    light8 = bproc.types.Light()
    # light.set_location([2, -2, 2])
    # light2.set_location([3, -2, 2])
    light3.set_location([4, 6, 3])
    light4.set_location([5.5, 6, 3])
    # light5.set_location([2, -3, 2])
    # light6.set_location([3, -3, 2])
    light7.set_location([4, 3.5, 3])
    light8.set_location([5.5, 3.5, 2])
    # light.set_energy(strength)
    # light2.set_energy(strength)
    light3.set_energy(strength)
    light4.set_energy(strength)
    # light5.set_energy(strength)
    # light6.set_energy(strength)
    light7.set_energy(strength)
    light8.set_energy(strength)


room_light(120)

poi = [4.3, 4.6, 0.8]
bproc.camera.set_resolution(640, 480)

locations= [[3.6, -2.0, 1.2], [3.6, -2.3, 1.2], [3.6, -2.6, 1.2], [3.6, -2.9, 1.2], [3.6, -2.0, 1.2], [3.6, -2.3, 1.2],
           [3.6, -2.6, 1.5], [3.6, -2.9, 1.5], [3.8, -2.0, 1.0], [3.8, -2.3, 1.0], [3.8, -2.6, 1.0], [3.8, -2.9, 1.0],
           [3.8, -2.0, 1.5], [3.8, -2.3, 1.5], [3.8, -2.6, 1.5], [3.8, -2.9, 1.5]]

def hide():
    for item in lob:
        item.blender_obj.hide_render = True


def camera_poses():
    for location in locations:
        # Sample random camera location above objects
        #location = np.random.uniform([3.1, -2.4, 1.0], [3.5, -2.5, 1.4])
        location = location
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - np.array(location), inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

def camera_poses_random(x):
    for i in range(x):
        location = np.random.uniform([3.4, 5, 1.0], [3.0, 4, 1.4])
        #location = location
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - np.array(location),
                                                                 inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)


def swap_location(obj_to_be_moved, new):
    obj_z = obj_to_be_moved.get_location()[2]
    new_location = [new[0], new[1], obj_z]
    obj_to_be_moved.set_location(new_location)


def deploy_scene(x):
    for i in range(x):
        for item in objs:
            item.blender_obj.hide_render = False

        for item in lob:
            item.blender_obj.hide_render = True

        random.shuffle(list_of_positions)
        random.shuffle(lob)

        random_objects = random.sample(lob, 4)
        for objects in random_objects:
            objects.blender_obj.hide_render = False

        print(random_objects)
        new_list = zip(random_objects, list_of_positions)


        for item in new_list:
            swap_location(item[0], item[1])

        for item in random_objects:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            x_mov = np.random.uniform([4.2], [4.6])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)
            item.set_location([x_mov, item.get_location()[1], item.get_location()[2]])
            print(item.get_name())
            print(item.get_cp("category_id"))

            # Render the scene
        data = bproc.renderer.render()
            # Write the rendering into an hdf5 file

        for item in objs:
            item.blender_obj.hide_render = True

        for objects in random_objects:
            objects.blender_obj.hide_render = False

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join(output_path, 'coco_data'),
                                                    instance_segmaps=seg_data["instance_segmaps"],
                                                    instance_attribute_maps=seg_data["instance_attribute_maps"],
                                                    colors=data["colors"],
                                                    color_file_format="JPEG",  mask_encoding_format="polygon")
        bproc.writer.write_hdf5(output_path, data)


def pipeline():
    camera_poses_random(5)
    deploy_scene(1000)


pipeline()