import os

import cv2
import json
def test1():

    f = open("/home/sorin/data/blenderproc/output2/coco_data/coco_annotations.json")
    data = json.load(f)
    anns = data["annotations"]
    print(data["categories"])


def create_list_from_id2json():
    with open('/home/sorin/code/blenderproc/data/id2name.json') as json_file:
        data = json.load(json_file)

    val = list(data.values())
    i = 0
    new_list = []
    for a in val:
        if a.startswith("suturo"):
            item = a.split(":")
            item_to_list = (item[1]).replace("'", "")
            new_list.append(item_to_list)
        i = i + 1

    return new_list


def get_id_of_object(obj):
    with open('/home/sorin/code/blenderproc/data/id2name.json') as json_file:
        data = json.load(json_file)

    val = list(data.values())
    i = 0
    for item in val:
        if item.endswith(obj + "'"):
            id_of_obj = i
            print(id_of_obj)
        else:
            i = i + 1


