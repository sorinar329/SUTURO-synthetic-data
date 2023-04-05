import blenderproc as bproc
import numpy as np
import os
import shutil
import pydevd_pycharm
#pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)
shutil.rmtree("/home/sorin/code/blenderproc/output/coco_data")
bproc.init()

# Create a simple object:
objs = bproc.loader.load_obj("/home/sorin/code/blenderproc/data/saved_scenes/suturobocup_scene_objects_on_table2.obj")
for j, obj in enumerate(objs):
    obj.set_cp("category_id", j+1)

# Initialization of perceiving objects
furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)
cracker_box = bproc.filter.one_by_attr(objs, "name", "Cracker_box")
sugar_box = bproc.filter.one_by_attr(objs, "name", "Sugar_box")
mustard_bottle = bproc.filter.one_by_attr(objs, "name", "Mustard_bottle")
softball = bproc.filter.one_by_attr(objs, "name", "softball")
pudding_box = bproc.filter.one_by_attr(objs, "name", "pudding_box")
gelatine_box = bproc.filter.one_by_attr(objs, "name", "gelatine_box")
# Create a point light next to it
light = bproc.types.Light()
light.set_location([2, -2, 2])
light.set_energy(300)

# Find point of interest, all cam poses should look towards it
poi = bproc.object.compute_poi(objs)
print(poi)
# Sample five camera poses
for i in range(10):
    # Sample random camera location above objects
    location = np.random.uniform([2, -1, 1.2], [3, -4, 1.2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0, 0))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)

# Movement on Y-Axis right from shelf
for i in range(10):
    # Sample random camera location above objects
    location = np.random.uniform([2.5,-4.2,1.2], [5, -4.2, 1.2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)

# Movement on Y-Axis left from shelf.
for i in range(10):
    # Sample random camera location above objects
    location = np.random.uniform([2.5, -0.8, 1.2], [5, -0.8, 1.2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0,0))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)

for i in range(3):
    cracker_box_location = np.random.uniform([0, 0, 0], [1.3, 0, 0])
    sugar_box_location = np.random.uniform([-0.15, 0, 0], [1.15, 0, 0])
    softball_location = np.random.uniform([-0.3, 0, 0], [1, 0, 0])
    mustard_bottle_location = np.random.uniform([-0.45, 0, 0], [0.85, 0, 0])
    pudding_box_location = np.random.uniform([-0.55, 0, 0], [0.7, 0, 0])
    gelatine_box_location = np.random.uniform([-0.7, 0, 0], [0.6, 0, 0])

    cracker_box.set_location(cracker_box_location)
    mustard_bottle.set_location(mustard_bottle_location)
    softball.set_location(softball_location)
    sugar_box.set_location(sugar_box_location)
    pudding_box.set_location(pudding_box_location)
    gelatine_box.set_location(gelatine_box_location)
    # Movement on X-Axis.

    seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
    # Render the scene
    data = bproc.renderer.render()
    # Write the rendering into an hdf5 file
    bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output", 'coco_data'),
                                        instance_segmaps=seg_data["instance_segmaps"],
                                        instance_attribute_maps=seg_data["instance_attribute_maps"],
                                        colors=data["colors"],
                                        color_file_format="JPEG")
    bproc.writer.write_hdf5("output/", data)

for i in range(3):
    cracker_box_location = np.random.uniform([0, 0, 0], [0, 0.8, 0])
    sugar_box_location = np.random.uniform([0, -0.2, 0], [0, 0.6, 0])
    softball_location = np.random.uniform([0, -0.4, 0], [0, 0.4, 0])
    mustard_bottle_location = np.random.uniform([0, -0.6, 0], [0, 0.2, 0])
    pudding_box_location = np.random.uniform([0, -0.7, 0], [0, 0.1, 0])
    gelatine_box_location = np.random.uniform([0, -0.8, 0], [0, 0, 0])

    cracker_box.set_location(cracker_box_location)
    mustard_bottle.set_location(mustard_bottle_location)
    softball.set_location(softball_location)
    sugar_box.set_location(sugar_box_location)
    pudding_box.set_location(pudding_box_location)
    gelatine_box.set_location(gelatine_box_location)
    # Movement on X-Axis.

    seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
    # Render the scene
    data = bproc.renderer.render()
    # Ignores objects for the coco annotations.
    for obj in furnitures:
        obj.blender_obj.hide_render = True
    # Write the rendering into an hdf5 file
    bproc.writer.write_coco_annotations(os.path.join("/home/sorin/code/blenderproc/output", 'coco_data'),
                                        instance_segmaps=seg_data["instance_segmaps"],
                                        instance_attribute_maps=seg_data["instance_attribute_maps"],
                                        colors=data["colors"],
                                        color_file_format="JPEG")
    bproc.writer.write_hdf5("output/", data)

