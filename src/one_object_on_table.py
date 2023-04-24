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
objs = bproc.loader.load_blend("/home/sorin/data/blenderproc/data/saved_scenes/one_object_on_table.blend")
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
plate = bproc.filter.one_by_attr(objs, "name", "Plate")
object_list.append(cracker_box)
object_list.append(plate)
object_list.append(bowl)


# second objects
cup = bproc.filter.one_by_attr(objs, "name", "Cup")
cup.set_scale([0.8, 0.8, 0.8])
tuna_can = bproc.filter.one_by_attr(objs, "name", "TunaFishCan")
tomato_soup = bproc.filter.one_by_attr(objs, "name", "TomatoSoupCan")
object_list.append(cup)
object_list.append(tuna_can)
object_list.append(tomato_soup)

# third objects
pudding_box = bproc.filter.one_by_attr(objs, "name", "JelloBox")
spoon = bproc.filter.one_by_attr(objs, "name", "Spoon")
knife = bproc.filter.one_by_attr(objs, "name", "Knife")
object_list.append(pudding_box)
object_list.append(knife)
object_list.append(spoon)

# fourth objects
pear = bproc.filter.one_by_attr(objs, "name", "Pear")
lemon = bproc.filter.one_by_attr(objs, "name", "Lemon")
gelatine_box = bproc.filter.one_by_attr(objs, "name", "JellOStrawberryBox")
object_list.append(pear)
object_list.append(lemon)
object_list.append(gelatine_box)

# fifth objects
apple = bproc.filter.one_by_attr(objs, "name", "Apple")
strawberry = bproc.filter.one_by_attr(objs, "name", "Strawberry")
mustard_bottle = bproc.filter.one_by_attr(objs, "name", "MustardBottle")
object_list.append(apple)
object_list.append(mustard_bottle)
object_list.append(strawberry)


#sixth objects
coffe_can = bproc.filter.one_by_attr(objs, "name", "CoffeeCan")
banana = bproc.filter.one_by_attr(objs, "name", "Banana")
fork = bproc.filter.one_by_attr(objs, "name", "Fork")
object_list.append(coffe_can)
object_list.append(banana)
object_list.append(fork)

# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 2])
light.set_energy(300)

# Find point of interest, all cam poses should look towards it
#poi = bproc.object.compute_poi(objs)
poi = [5, -2.6, 0.8]
bproc.camera.set_resolution(640, 480)
print(poi)
rotation = np.random.uniform([0, 0, 0], [0, 0, 6])
def hide():
    for item in object_list:
        item.blender_obj.hide_render = True

def camer_poses(x):
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([2, -1, 0.8], [3, -4, 2.5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0, 0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

    # Movement on Y-Axis right from shelf
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([3,-4.2,0.8], [5.3, -4.2, 2.5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)

    # Movement on Y-Axis left from shelf.
    for i in range(x):
        # Sample random camera location above objects
        location = np.random.uniform([3, -0.5, 0.8], [5.3, -0.5, 2.5])
        # Compute rotation based on vector going from location towards poi
        rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
        # Add homog cam pose based on location an rotation
        cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
        bproc.camera.add_camera_pose(cam2world_matrix)


def deploy_scene(x):

    for item in object_list:
        hide()
        item.blender_obj.hide_render = False
        for i in range(x):
            random_location = np.random.uniform([4.5, -2.34, item.get_location()[2]], [5.5, -2.84, item.get_location()[2]])
            item.set_location(random_location)
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
    camer_poses(6)
    deploy_scene(3)


pipeline()

