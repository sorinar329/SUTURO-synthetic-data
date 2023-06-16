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
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
objs = bproc.loader.load_blend("/home/sorin/data/blenderproc/data/saved_scenes/storing_groceries_table.blend")
output_path="/home/sorin/code/blenderproc/output"
#shutil.rmtree(output_path + "/coco_data")


for j, obj in enumerate(objs):
    obj_list = utils.create_list_from_id2json()
    print(obj.get_name())
    if obj.get_name() in obj_list:
        obj_id = utils.get_id_of_object(obj.get_name())
        obj.set_cp("category_id", obj_id)
    else:
        obj.set_cp("category_id", j + 10000)

furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)


def init_objects():
    cracker_box = bproc.filter.one_by_attr(objs, "name", "CrackerBox")
    tuna_can = bproc.filter.one_by_attr(objs, "name", "TunaFishCan")
    tomato_soup = bproc.filter.one_by_attr(objs, "name", "TomatoSoupCan")
    pudding_box = bproc.filter.one_by_attr(objs, "name", "JelloBox")
    pear = bproc.filter.one_by_attr(objs, "name", "Pear")
    lemon = bproc.filter.one_by_attr(objs, "name", "Lemon")
    gelatine_box = bproc.filter.one_by_attr(objs, "name", "JellOStrawberryBox")
    apple = bproc.filter.one_by_attr(objs, "name", "Apple")
    strawberry = bproc.filter.one_by_attr(objs, "name", "Strawberry")
    mustard_bottle = bproc.filter.one_by_attr(objs, "name", "MustardBottle")
    coffe_can = bproc.filter.one_by_attr(objs, "name", "CoffeeCan")
    banana = bproc.filter.one_by_attr(objs, "name", "Banana")
    milk = bproc.filter.one_by_attr(objs, "name", "MilkPack")
    cereal_box = bproc.filter.one_by_attr(objs, "name", "CerealBox")
    bowl = bproc.filter.one_by_attr(objs, "name", "Bowl")
    spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")

    list_of_objects = [cracker_box, tuna_can, tomato_soup, pudding_box, pear, lemon, gelatine_box, apple, strawberry,
                       mustard_bottle, coffe_can, banana, milk, cereal_box, spoon, bowl]

    return list_of_objects


lob = init_objects()


def positions():
    first_pos = [4.5, -2.23]
    second_pos = [4.5, -2.46]
    third_pos = [4.5, -2.67]
    fourth_pos = [4.5, -2.86]
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


room_light(50)

poi = [4.5, -2.5, 0.9]
bproc.camera.set_resolution(640, 480)
print(poi)

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


def swap_location(obj_to_be_moved, new):
    obj_z = obj_to_be_moved.get_location()[2]
    new_location = [new[0], new[1], obj_z]
    obj_to_be_moved.set_location(new_location)


def deploy_scene(x):
    for i in range(x):
        hide()
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
            x_mov = np.random.uniform([4.5], [4.9])
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
    camera_poses()
    deploy_scene(30)


pipeline()