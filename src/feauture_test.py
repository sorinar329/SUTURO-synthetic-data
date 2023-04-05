import blenderproc as bproc
import numpy as np
import os
import shutil
import pydevd_pycharm
#pydevd_pycharm.settrace('localhost', port=12345, stdoutToServer=True, stderrToServer=True)
#shutil.rmtree("/home/sorin/code/blenderproc/output2/coco_data")
bproc.init()

# Create a simple object:
objs = bproc.loader.load_obj("/home/sorin/data/blenderproc/data/saved_scenes/testing.obj")
for j, obj in enumerate(objs):
    obj.set_cp("category_id", j+1)

furnitures = bproc.filter.by_attr(objs, "name", "Furniture.*", regex=True)
light = bproc.types.Light()
light.set_location([2, -2, 2])
light.set_energy(300)

# Find point of interest, all cam poses should look towards it
poi = bproc.object.compute_poi(objs)
print(poi)
# Sample five camera poses
for i in range(1):
    # Sample random camera location above objects
    location = np.random.uniform([2, -1, 1.2], [3, -4, 1.2])
    # Compute rotation based on vector going from location towards poi
    rotation_matrix = bproc.camera.rotation_from_forward_vec(poi - location, inplane_rot=np.random.uniform(0, 0))
    # Add homog cam pose based on location an rotation
    cam2world_matrix = bproc.math.build_transformation_mat(location, rotation_matrix)
    bproc.camera.add_camera_pose(cam2world_matrix)


data = bproc.renderer.render()
for obj in furnitures:
    obj.blender_obj.hide_render = True


seg_data = bproc.renderer.render_segmap(map_by=["instance", "class", "name"])
bproc.writer.write_coco_annotations(os.path.join("/home/sorin/data/blenderproc/output2", 'coco_data'),
                                        instance_segmaps=seg_data["instance_segmaps"],
                                        instance_attribute_maps=seg_data["instance_attribute_maps"],
                                        colors=data["colors"],
                                        color_file_format="JPEG")
bproc.writer.write_hdf5("/home/sorin/data/blenderproc/output2/", data)