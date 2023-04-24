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
first_list = []
second_list = []
third_list = []
fourth_list = []
fifth_list = []
sixth_list = []
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
# Create a simple object:
#objs = bproc.loader.load_obj("/home/sorin/data/blenderproc/data/saved_scenes/objects_on_table_final_18_objects.obj")
objs = bproc.loader.load_blend("/home/sorin/data/blenderproc/data/saved_scenes/objects_on_table_final_18_objects_new_textures.blend")
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

# Initialization of perceiving objects
furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)
# Definition of the objects in the scene from bottom left of the table to top right (as seen from z)
# first objects
cracker_box = bproc.filter.one_by_attr(objs, "name", "CrackerBox")
bowl = bproc.filter.one_by_attr(objs, "name", "Bowl")
bowl.set_scale([0.8, 0.8, 0.8])
plate = bproc.filter.one_by_attr(objs, "name", "Plate")
plate.set_scale([0.8, 0.8, 0.8])
first_list.append(cracker_box)
first_list.append(plate)
first_list.append(bowl)

# second objects
cup = bproc.filter.one_by_attr(objs, "name", "Cup")
cup.set_scale([0.8, 0.8, 0.8])
tuna_can = bproc.filter.one_by_attr(objs, "name", "TunaFishCan")
tomato_soup = bproc.filter.one_by_attr(objs, "name", "TomatoSoupCan")
second_list.append(cup)
second_list.append(tuna_can)
second_list.append(tomato_soup)

# third objects
pudding_box = bproc.filter.one_by_attr(objs, "name", "JelloBox")
spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")
spoon.set_scale([0.8, 0.8, 0.8])
knife = bproc.filter.one_by_attr(objs, "name", "Knife")
knife.set_scale([0.8, 0.8, 0.8])
third_list.append(pudding_box)
third_list.append(knife)
third_list.append(spoon)

# fourth objects
pear = bproc.filter.one_by_attr(objs, "name", "Pear")
lemon = bproc.filter.one_by_attr(objs, "name", "Lemon")
gelatine_box = bproc.filter.one_by_attr(objs, "name", "JellOStrawberryBox")
fourth_list.append(pear)
fourth_list.append(lemon)
fourth_list.append(gelatine_box)

# fifth objects
apple = bproc.filter.one_by_attr(objs, "name", "Apple")
strawberry = bproc.filter.one_by_attr(objs, "name", "Strawberry")
mustard_bottle = bproc.filter.one_by_attr(objs, "name", "MustardBottle")
fifth_list.append(apple)
fifth_list.append(mustard_bottle)
fifth_list.append(strawberry)


#sixth objects
coffe_can = bproc.filter.one_by_attr(objs, "name", "CoffeeCan")
banana = bproc.filter.one_by_attr(objs, "name", "Banana")
fork = bproc.filter.one_by_attr(objs, "name", "Fork")
fork.set_scale([0.8, 0.8, 0.8])
sixth_list.append(coffe_can)
sixth_list.append(banana)
sixth_list.append(fork)

# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 2])
light.set_energy(200)

# Find point of interest, all cam poses should look towards it
#poi = bproc.object.compute_poi(objs)
poi = [5, -2.6, 0.8]
bproc.camera.set_resolution(640, 480)
print(poi)

def hide_all():
    for item in first_list:
        item.blender_obj.hide_render = True

    for item in sixth_list:
        item.blender_obj.hide_render = True

    for item in second_list:
        item.blender_obj.hide_render = True

    for item in fifth_list:
        item.blender_obj.hide_render = True

    for item in third_list:
        item.blender_obj.hide_render = True

    for item in fourth_list:
        item.blender_obj.hide_render = True
# Sample the camera poses.
def camer_poses(x):
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([2, -1, 1.0], [3, -4, 2.5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

    # Movement on Y-Axis right from shelf
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([3,-4.2,1.0], [5.3, -4.2, 2.5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

    # Movement on Y-Axis left from shelf.
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([3, -0.5, 1.0], [5.3, -0.5, 2.5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

def get_initial_position(obj):
    inital_pos = obj.get_location()
    return inital_pos

def first_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.1, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[0]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = second_list[0]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = third_list[0]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = fourth_list[0]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = fifth_list[0]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = sixth_list[0]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)

    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [0, 0.7, 0])
        second_location = np.random.uniform([0, -0.1, 0], [0, 0.5, 0])
        third_location = np.random.uniform([0, -0.3, 0], [0, 0.3, 0])
        fourth_location = np.random.uniform([0, -0.5, 0], [0, 0.1, 0])
        fifth_location = np.random.uniform([0, -0.6, 0], [0, 0.0, 0])
        sixth_location = np.random.uniform([0, -0.7, 0], [0, 0, 0])
        for item in first_list:
            item.blender_obj.hide_render = True

        hide_all()

        far_left_bottom_object = first_list[0]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = second_list[0]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = third_list[0]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = fourth_list[0]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = fifth_list[0]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = sixth_list[0]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)

def second_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.1, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[1]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = second_list[1]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = third_list[1]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = fourth_list[1]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = fifth_list[1]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = sixth_list[1]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)

    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [0, 0.7, 0])
        second_location = np.random.uniform([0, -0.1, 0], [0, 0.5, 0])
        third_location = np.random.uniform([0, -0.3, 0], [0, 0.3, 0])
        fourth_location = np.random.uniform([0, -0.5, 0], [0, 0.1, 0])
        fifth_location = np.random.uniform([0, -0.6, 0], [0, 0.0, 0])
        sixth_location = np.random.uniform([0, -0.7, 0], [0, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[1]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = second_list[1]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = third_list[1]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = fourth_list[1]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = fifth_list[1]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = sixth_list[1]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)


def third_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.1, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[2]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = second_list[2]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = third_list[2]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = fourth_list[2]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = fifth_list[2]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = sixth_list[2]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)

    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [0, 0.7, 0])
        second_location = np.random.uniform([0, -0.1, 0], [0, 0.5, 0])
        third_location = np.random.uniform([0, -0.3, 0], [0, 0.3, 0])
        fourth_location = np.random.uniform([0, -0.5, 0], [0, 0.1, 0])
        fifth_location = np.random.uniform([0, -0.6, 0], [0, 0.0, 0])
        sixth_location = np.random.uniform([0, -0.7, 0], [0, 0, 0])
        for item in first_list:
            item.blender_obj.hide_render = True

        hide_all()

        far_left_bottom_object = first_list[2]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = second_list[2]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = third_list[2]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = fourth_list[2]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = fifth_list[2]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = sixth_list[2]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)


def random_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.1, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = random.choice(first_list)
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object.set_location(far_left_bottom_object.get_location() + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = random.choice(second_list)
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(left_bottom_object.get_location() + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = random.choice(third_list)
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(mid_left_object.get_location() + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = random.choice(fourth_list)
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(mid_right_object.get_location() + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = random.choice(fifth_list)
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(mid_top_object.get_location() + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = random.choice(sixth_list)
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(far_mid_top_object.get_location() + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [0, 0.7, 0])
        second_location = np.random.uniform([0, -0.1, 0], [0, 0.5, 0])
        third_location = np.random.uniform([0, -0.3, 0], [0, 0.3, 0])
        fourth_location = np.random.uniform([0, -0.5, 0], [0, 0.1, 0])
        fifth_location = np.random.uniform([0, -0.6, 0], [0, 0.0, 0])
        sixth_location = np.random.uniform([0, -0.7, 0], [0, 0, 0])


        hide_all()

        far_left_bottom_object = random.choice(first_list)
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object_initial_pos = far_left_bottom_object.get_location()
        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos + first_location)
        far_left_bottom_object.set_rotation_euler(far_left_bottom_object.get_rotation_euler() + rotation)

        left_bottom_object = random.choice(second_list)
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object_initial_pos = left_bottom_object.get_location()
        left_bottom_object.set_location(left_bottom_object_initial_pos + second_location)
        left_bottom_object.set_rotation_euler(left_bottom_object.get_rotation_euler() + rotation)

        mid_left_object = random.choice(third_list)
        mid_left_object.blender_obj.hide_render = False
        mid_left_object_initial_pos = mid_left_object.get_location()
        mid_left_object.set_location(mid_left_object_initial_pos + third_location)
        mid_left_object.set_rotation_euler(mid_left_object.get_rotation_euler() + rotation)

        mid_right_object = random.choice(fourth_list)
        mid_right_object.blender_obj.hide_render = False
        mid_right_object_initial_pos = mid_right_object.get_location()
        mid_right_object.set_location(mid_right_object_initial_pos + fourth_location)
        mid_right_object.set_rotation_euler(mid_right_object.get_rotation_euler() + rotation)

        mid_top_object = random.choice(fifth_list)
        mid_top_object.blender_obj.hide_render = False
        mid_top_object_initial_pos = mid_top_object.get_location()
        mid_top_object.set_location(mid_top_object_initial_pos + fifth_location)
        mid_top_object.set_rotation_euler(mid_top_object.get_rotation_euler() + rotation)

        far_mid_top_object = random.choice(sixth_list)
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object_initial_pos = far_mid_top_object.get_location()
        far_mid_top_object.set_location(far_mid_top_object_initial_pos + sixth_location)
        far_mid_top_object.set_rotation_euler(far_mid_top_object.get_rotation_euler() + rotation)
        # Movement on X-Axis.

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

        far_left_bottom_object.set_location(far_left_bottom_object_initial_pos)
        left_bottom_object.set_location(left_bottom_object_initial_pos)
        mid_left_object.set_location(mid_left_object_initial_pos)
        mid_right_object.set_location(mid_right_object_initial_pos)
        mid_top_object.set_location(mid_top_object_initial_pos)
        far_mid_top_object.set_location(far_mid_top_object_initial_pos)


def pipeline():
    camer_poses(8)
    first_objects(8)
    second_objects(8)
    third_objects(8)
    #random_objects(12)

pipeline()