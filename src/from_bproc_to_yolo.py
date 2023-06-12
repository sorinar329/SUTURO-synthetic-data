import utils

path_to_json_id = "/home/sorin/code/blenderproc/data/id2name.json"
path_to_json_coco = "/home/sorin/code/blenderproc/09_06_sg/coco_data/coco_annotations.json"
old_dir = "/home/sorin/code/blenderproc/09_06_sg/coco_data/images/"
new_dir = "/home/sorin/data/09_06_storing_groceries"


def pipeline_from_output_to_yolo(json_id, json_coco, old_dir, new_dir):
    utils.convert_coco_to_yolo(json_coco, new_dir)
    utils.move_images_to_new_dir(old_dir, new_dir)
    utils.rename_images(path=new_dir + "/images/", i = 0)
    utils.trainsplit(new_dir + "/")
    utils.write_data_yaml(json_id, new_dir)


pipeline_from_output_to_yolo(path_to_json_id, path_to_json_coco, old_dir, new_dir)