import json
import os
import blenderproc as bproc

def create_list_from_id2json(path='/home/sorin/code/blenderproc/data/id2name.json'):
    with open(path) as json_file:
        data = json.load(json_file)

    val = list(data.values())
    i = 0
    new_list = []
    for a in val:
        if a.startswith("suturo") or a.startswith("soma"):
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
            return id_of_obj
        else:
            i = i + 1



