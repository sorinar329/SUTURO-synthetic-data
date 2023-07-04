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
objs = bproc.loader.load_blend("/home/sorin/blenderdata/blender_data/robocup/scenes/arena_wired_shelf.blend")
output_path="/home/sorin/code/blenderproc/wired_shelf"
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
        print("False")
        print(obj.get_name())





#furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)


def init_objects():
    cracker_box = bproc.filter.one_by_attr(objs, "name", "CrackerBox")
    tuna_can = bproc.filter.one_by_attr(objs, "name", "TunaFishCan")
    tomato_soup = bproc.filter.one_by_attr(objs, "name", "TomatoSoupCan")
    pudding_box = bproc.filter.one_by_attr(objs, "name", "JelloBox")
    lemon = bproc.filter.one_by_attr(objs, "name", "Lemon")
    lemon1 = bproc.filter.one_by_attr(objs, "name", "Lemon.001")
    gelatine_box = bproc.filter.one_by_attr(objs, "name", "JellOStrawberryBox")
    apple = bproc.filter.one_by_attr(objs, "name", "Apple")
    apple1 = bproc.filter.one_by_attr(objs, "name", "Apple.001")
    banana1 = bproc.filter.one_by_attr(objs, "name", "Banana.001")
    strawberry = bproc.filter.one_by_attr(objs, "name", "Strawberry")
    mustard_bottle = bproc.filter.one_by_attr(objs, "name", "MustardBottle")
    coffe_can = bproc.filter.one_by_attr(objs, "name", "CoffeeCan")
    banana = bproc.filter.one_by_attr(objs, "name", "Banana")
    bowl = bproc.filter.one_by_attr(objs, "name", "Bowl")
    spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")
    fork = bproc.filter.one_by_attr(objs, "name", "Fork")

    meat_can = bproc.filter.one_by_attr(objs, "name", "MeatCan")
    cup = bproc.filter.one_by_attr(objs, "name", "MetalMug")
    plate = bproc.filter.one_by_attr(objs, "name", "MetalPlate")
    orange = bproc.filter.one_by_attr(objs, "name", "Orange")
    orange1 = bproc.filter.one_by_attr(objs, "name", "Orange.001")
    peach = bproc.filter.one_by_attr(objs, "name", "Peach")
    pear = bproc.filter.one_by_attr(objs, "name", "Pear")
    pear1 = bproc.filter.one_by_attr(objs, "name", "Pear.001")
    plum = bproc.filter.one_by_attr(objs, "name", "Plum")
    pringles = bproc.filter.one_by_attr(objs, "name", "PringlesChipsCan")
    sugar_box = bproc.filter.one_by_attr(objs, "name", "SugarBox")

    list_of_objects = [cracker_box, tuna_can, tomato_soup, pudding_box, pear, lemon, gelatine_box, apple, strawberry,
                       mustard_bottle, coffe_can, banana, spoon, bowl, plum, plate, pringles, pear1,
                       peach, lemon1, apple1, banana1, banana, fork, meat_can, cup, orange, orange1, sugar_box]

    return list_of_objects


lob = init_objects()


def define_shelf_pos():
    shelf_top = []
    shelf_bottom = []
    shelf_mid = []
    for obj in lob:
        if 0.7 > obj.get_location()[2] > 0.3:
            shelf_mid.append(obj)
        elif obj.get_location()[2] > 0.7:
            shelf_top.append(obj)
        else:
            shelf_bottom.append(obj)

    return shelf_top, shelf_mid, shelf_bottom

def positions():
    first_pos = [6.3, 0.35]
    second_pos = [6.0, 0.35]
    third_pos = [5.7, 0.35]
    pos_list = [first_pos, second_pos, third_pos]
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
    light3.set_location([7.6, 1, 3])
    light4.set_location([4.6, 1, 3])
    # light5.set_location([2, -3, 2])
    # light6.set_location([3, -3, 2])
    light7.set_location([7.6, -1, 3])
    light8.set_location([4.6, -1, 3])
    # light.set_energy(strength)
    # light2.set_energy(strength)
    light3.set_energy(strength)
    light4.set_energy(strength)
    # light5.set_energy(strength)
    # light6.set_energy(strength)
    light7.set_energy(strength)
    light8.set_energy(strength)


room_light(120)

poi = [[5.95, 0.3, 1.1], [5.95, 0.35, 0.6], [5.95, 0.35, 0.3]]
bproc.camera.set_resolution(640, 480)

locations= [[3.6, -2.0, 1.2], [3.6, -2.3, 1.2], [3.6, -2.6, 1.2], [3.6, -2.9, 1.2], [3.6, -2.0, 1.2], [3.6, -2.3, 1.2],
           [3.6, -2.6, 1.5], [3.6, -2.9, 1.5], [3.8, -2.0, 1.0], [3.8, -2.3, 1.0], [3.8, -2.6, 1.0], [3.8, -2.9, 1.0],
           [3.8, -2.0, 1.5], [3.8, -2.3, 1.5], [3.8, -2.6, 1.5], [3.8, -2.9, 1.5]]

def hide():
    for item in lob:
        item.blender_obj.hide_render = True


def camera_poses_random(x):
    for i in range(x):
        for p in poi:
            location = np.random.uniform([5.3, 1.1, 1.0], [6.5, 1.5, 1.4])
            #location = location
            # Compute rotation based on vector going from location towards poi
            rotation_matrix = bproc.camera.rotation_from_forward_vec(p - np.array(location),
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
    shelf_top, shelf_mid, shelf_bottom = define_shelf_pos()
    for i in range(x):
        for item in objs:
            item.blender_obj.hide_render = False

        hide()
        random.shuffle(list_of_positions)
        random.shuffle(shelf_bottom)
        random.shuffle(shelf_top)
        random.shuffle(shelf_mid)
        random_objects1 = random.sample(shelf_top, 3)
        for obj in random_objects1:
            print(obj.get_name())
        random_objects2 = random.sample(shelf_bottom, 3)
        random_objects3 = random.sample(shelf_mid, 3)
        for objects in random_objects1:
            objects.blender_obj.hide_render = False

        for objects in random_objects2:
            objects.blender_obj.hide_render = False

        for objects in random_objects3:
            objects.blender_obj.hide_render = False


        new_list1 = zip(random_objects1, list_of_positions)
        new_list2 = zip(random_objects2, list_of_positions)
        new_list3 = zip(random_objects3, list_of_positions)

        for item in new_list1:
            swap_location_shelf(item[0], item[1])

        for item in new_list2:
            swap_location_shelf(item[0], item[1])

        for item in new_list3:
            swap_location_shelf(item[0], item[1])

        for item in random_objects1:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)

        for item in random_objects2:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)

        for item in random_objects3:
            rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
            item.set_rotation_euler(item.get_rotation_euler() + rotation)


            # Render the scene
        data = bproc.renderer.render()
        # Write the rendering into an hdf5 file

        for item in objs:
            item.blender_obj.hide_render = True

        for objects in random_objects1:
            objects.blender_obj.hide_render = False

        for objects in random_objects2:
            objects.blender_obj.hide_render = False

        for objects in random_objects3:
            objects.blender_obj.hide_render = False

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join(output_path, 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5(output_path, data)


def pipeline():
    camera_poses_random(10)
    deploy_scene(1)


pipeline()
