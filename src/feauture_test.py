import blenderproc as bproc
import numpy as np
import os
import random
import shutil
import json
import sys
sys.path.append("/home/sorin/code/blenderproc/src")
import utils
shutil.rmtree("/home/sorin/code/blenderproc/output2/coco_data")
bproc.init()
first_list = []
second_list = []
third_list = []
fourth_list = []
fifth_list = []
sixth_list = []
# Create a simple object:
objs = bproc.loader.load_obj("/home/sorin/data/blenderproc/data/saved_scenes/objects_on_table_final_18_objects.obj")

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
plate = bproc.filter.one_by_attr(objs, "name", "Plate")
first_list.append(cracker_box)
first_list.append(plate)
first_list.append(bowl)

# second objects
cup = bproc.filter.one_by_attr(objs, "name", "Cup")
tuna_can = bproc.filter.one_by_attr(objs, "name", "TunaFishCan")
tomato_soup = bproc.filter.one_by_attr(objs, "name", "TomatoSoupCan")
second_list.append(cup)
second_list.append(tuna_can)
second_list.append(tomato_soup)

# third objects
pudding_box = bproc.filter.one_by_attr(objs, "name", "JelloBox")
spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")
knife = bproc.filter.one_by_attr(objs, "name", "Knife")
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
sixth_list.append(coffe_can)
sixth_list.append(banana)
sixth_list.append(fork)

# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 2])
light.set_energy(300)

# Find point of interest, all cam poses should look towards it
poi = bproc.object.compute_poi(objs)
print(poi)
print(first_list)
print(second_list)
print(third_list)
print(fourth_list)
print(fifth_list)
print(sixth_list)
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
    for i in range(x+1):
        # Sample random camera location above objects
        location = np.random.uniform([2, -1, 1.2], [3, -4, 1.2])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

def first_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.2, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[0]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = second_list[0]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = third_list[0]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = fourth_list[0]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = fifth_list[0]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = sixth_list[0]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False

        # Render the scene
        data = bproc.renderer.render()
        # Write the rendering into an hdf5 file

        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("output2/", data)

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
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = second_list[0]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = third_list[0]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = fourth_list[0]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = fifth_list[0]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = sixth_list[0]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False
        # Render the scene
        data = bproc.renderer.render()
        # Ignores objects for the coco annotations.
        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
        # Write the rendering into an hdf5 file
        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("first_dataset_18_objects_on_table_7k/", data)

def second_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.2, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[1]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = second_list[1]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = third_list[1]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = fourth_list[1]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = fifth_list[1]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = sixth_list[1]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)

        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False

        # Render the scene
        data = bproc.renderer.render()
        # Write the rendering into an hdf5 file

        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("output2/", data)

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
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = second_list[1]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = third_list[1]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = fourth_list[1]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = fifth_list[1]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = sixth_list[1]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False
        # Render the scene
        data = bproc.renderer.render()
        # Ignores objects for the coco annotations.
        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
        # Write the rendering into an hdf5 file
        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("first_dataset_18_objects_on_table_7k/", data)


def third_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.2, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = first_list[2]
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = second_list[2]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = third_list[2]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = fourth_list[2]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = fifth_list[2]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = sixth_list[2]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False

        # Render the scene
        data = bproc.renderer.render()
        # Write the rendering into an hdf5 file

        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("output2/", data)

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
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = second_list[2]
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = third_list[2]
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = fourth_list[2]
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = fifth_list[2]
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = sixth_list[2]
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False
        # Render the scene
        data = bproc.renderer.render()
        # Ignores objects for the coco annotations.
        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
        # Write the rendering into an hdf5 file
        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("first_dataset_18_objects_on_table_7k/", data)


def random_objects(x):
    for i in range(x):
        first_location = np.random.uniform([0, 0, 0], [1.2, 0, 0])
        second_location = np.random.uniform([-0.05, 0, 0], [1.05, 0, 0])
        third_location = np.random.uniform([-0.2, 0, 0], [0.9, 0, 0])
        fourth_location = np.random.uniform([-0.35, 0, 0], [0.75, 0, 0])
        fifth_location = np.random.uniform([-0.45, 0, 0], [0.6, 0, 0])
        sixth_location = np.random.uniform([-0.6, 0, 0], [0.5, 0, 0])

        hide_all()

        far_left_bottom_object = random.choice(first_list)
        far_left_bottom_object.blender_obj.hide_render = False
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = random.choice(second_list)
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = random.choice(third_list)
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = random.choice(fourth_list)
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = random.choice(fifth_list)
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = random.choice(sixth_list)
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False

        # Render the scene
        data = bproc.renderer.render()
        # Write the rendering into an hdf5 file

        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])

        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("output2/", data)

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
        far_left_bottom_object.set_location(first_location)
        left_bottom_object = random.choice(second_list)
        left_bottom_object.blender_obj.hide_render = False
        left_bottom_object.set_location(second_location)
        mid_left_object = random.choice(third_list)
        mid_left_object.blender_obj.hide_render = False
        mid_left_object.set_location(third_location)
        mid_right_object = random.choice(fourth_list)
        mid_right_object.blender_obj.hide_render = False
        mid_right_object.set_location(fourth_location)
        mid_top_object = random.choice(fifth_list)
        mid_top_object.blender_obj.hide_render = False
        mid_top_object.set_location(fifth_location)
        far_mid_top_object = random.choice(sixth_list)
        far_mid_top_object.blender_obj.hide_render = False
        far_mid_top_object.set_location(sixth_location)
        # Movement on X-Axis.

        for obj in furnitures:
            obj.blender_obj.hide_render = False
        # Render the scene
        data = bproc.renderer.render()
        # Ignores objects for the coco annotations.
        for obj in furnitures:
            obj.blender_obj.hide_render = True

        seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
        # Write the rendering into an hdf5 file
        bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output2", 'coco_data'),
                                            instance_segmaps=seg_data["instance_segmaps"],
                                            instance_attribute_maps=seg_data["instance_attribute_maps"],
                                            colors=data["colors"],
                                            color_file_format="JPEG")
        bproc.writer.write_hdf5("first_dataset_18_objects_on_table_7k/", data)


def pipeline():
    camer_poses(2)
    #first_objects(2)
    #second_objects(2)
    #third_objects(2)
    random_objects(2)

pipeline()