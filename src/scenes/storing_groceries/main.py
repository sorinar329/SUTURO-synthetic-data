import blenderproc as bproc
import os
import random
import sys

import blenderproc.python.types.MeshObjectUtility
import numpy as np

sys.path.append("/home/naser/workspace/blender_synthetic_data/SUTURO-synthetic-data/src")
import path_utils
import utils
import yaml_config
from scenes import arguments, scene

args = arguments.get_argparse()

config = yaml_config.YAMLConfig(args.config_yaml)
bproc.init()
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
objs = bproc.loader.load_blend(path_utils.get_path_blender_scene("/home/naser/workspace/blender_data",
                                                                 "storing_groceries_shelf.blend"))

if args.output is None:
    output_path = path_utils.get_path_output_dir()

for j, obj in enumerate(objs):
    obj_list = utils.create_list_from_id2json()
    if obj.get_name() in obj_list:
        print(type(obj))
        obj_id = utils.get_id_of_object(obj.get_name())
        obj.set_cp("category_id", obj_id)
    else:
        obj.set_cp("category_id", j + 10000)

furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)

lob = scene.init_objects(config.get_objects(), objs)


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

locations = [[4, -2, 2], [5, -2, 2], [4, -3, 2], [5, -3, 2], [2.7, -3, 1.5]]
scene.set_homogeneous_lighting(locations=locations, strength=50)
bproc.camera.set_resolution(640, 480)


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
        scene.hide_object(lob)
        random.shuffle(list_of_positions)
        random.shuffle(shelf_bottom)
        random.shuffle(shelf_top)

        random_objects1 = random.sample(shelf_top, 4)
        random_objects2 = random.sample(shelf_bottom, 4)
        new_list1 = zip(random_objects1, list_of_positions)
        new_list2 = zip(random_objects2, list_of_positions)

        for item in new_list1:
            swap_location_shelf(item[0], item[1])

        for item in new_list2:
            swap_location_shelf(item[0], item[1])

        scene.set_rendering_of_object(random_objects1, False)
        scene.set_rendering_of_object(random_objects2, False)
        scene.set_random_rotation_zaxis(random_objects1)
        scene.set_random_rotation_zaxis()(random_objects2)
        scene.set_rendering_of_object(furnitures, False)

        # Render the scene
        data = bproc.renderer.render()
        # Write the rendering into an hdf5 file

        scene.set_rendering_of_object(furnitures, True)

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join(output_path, 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5(output_path, data)


def pipeline():
    scene.get_cam_poses(config.get_list_locations(), config.get_position_of_interest())
    deploy_scene(300)


pipeline()
