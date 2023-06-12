import blenderproc as bproc
import numpy as np
import os
import random
import sys

sys.path.append("/home/naser/workspace/blender_synthetic_data/SUTURO-synthetic-data/src")

import filepaths
import utils
import yaml_config

config = yaml_config.YAMLConfig("toy_config.yaml")
bproc.init()
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
objs = bproc.loader.load_blend(filepaths.get_path_blender_scene("/home/naser/workspace/blender_data",
                                                                  "storing_groceries_shelf.blend"))
output_path = filepaths.get_path_output_dir()
# shutil.rmtree(output_path + "/coco_data")




for j, obj in enumerate(objs):
    obj_list = utils.create_list_from_id2json()
    print(config)
    print(obj.get_name())
    if obj.get_name() in obj_list:
        obj_id = utils.get_id_of_object(obj.get_name())
        obj.set_cp("category_id", obj_id)
    else:
        obj.set_cp("category_id", j + 10000)

furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)


def init_objects():
    blender_objects = []
    for o in config.get_objects():
        blender_objects.append(bproc.filter.one_by_attr(objs, "name", o))

    return blender_objects


lob = init_objects()


def define_shelf_pos():
    shelf_top = []
    shelf_bottom = []
    for obj in lob:
        if obj.get_location()[2] < 0.65:
            shelf_bottom.append(obj)
        else:
            shelf_top.append(obj)

    return shelf_top, shelf_bottom

list_of_positions = config.get_list_positions()


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
    light3.set_location([4, -2, 2])
    light4.set_location([5, -2, 2])
    # light5.set_location([2, -3, 2])
    # light6.set_location([3, -3, 2])
    light7.set_location([4, -3, 2])
    light8.set_location([5, -3, 2])
    # light.set_energy(strength)
    # light2.set_energy(strength)
    light3.set_energy(strength)
    light4.set_energy(strength)
    # light5.set_energy(strength)
    # light6.set_energy(strength)
    light7.set_energy(strength)
    light8.set_energy(strength)
    light9 = bproc.types.Light()
    light9.set_location([2.7, -3, 1.5])
    light9.set_energy(70)


room_light(50)

bproc.camera.set_resolution(640, 480)

def hide():
    for item in lob:
        item.blender_obj.hide_render = True


def camera_poses():
    locations = config.get_list_locations()
    poi = config.get_position_of_interest()
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


def swap_location_shelf(obj_to_be_moved, new):
    obj_z = obj_to_be_moved.get_location()[2]
    obj_x = obj_to_be_moved.get_location()[0]
    new_location = [new[0], new[1], obj_z]
    print(obj_to_be_moved.get_name())
    print(new_location)
    obj_to_be_moved.set_location(new_location)


def deploy_scene(x):
    shelf_top, shelf_bottom = define_shelf_pos()
    for i in range(x):
        hide()
        random.shuffle(list_of_positions)
        random.shuffle(shelf_bottom)
        random.shuffle(shelf_top)

        random_objects1 = random.sample(shelf_top, 4)
        random_objects2 = random.sample(shelf_bottom, 4)
        for objects in random_objects1:
            objects.blender_obj.hide_render = False

        for objects in random_objects2:
            objects.blender_obj.hide_render = False

        new_list1 = zip(random_objects1, list_of_positions)
        new_list2 = zip(random_objects2, list_of_positions)

        for item in new_list1:
            swap_location_shelf(item[0], item[1])

        for item in new_list2:
            swap_location_shelf(item[0], item[1])

        for item in random_objects1:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)

        for item in random_objects2:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)

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
    camera_poses()
    deploy_scene(300)


pipeline()
