import json
import os
import shutil
from natsort import natsorted


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


def create_new_dir(parent_dir, name):
    new_dir = os.path.join(parent_dir + name)
    try:
        os.makedirs(new_dir, exist_ok=True)
        print("Directory '%s' created successfully" % name)
    except OSError as error:
        print("Directory '%s' can not be created" % name)
    os.mkdir(new_dir + "/train")
    os.mkdir(new_dir + "/train/labels")
    os.mkdir(new_dir + "/train/images")
    os.mkdir(new_dir + "/val")
    os.mkdir(new_dir + "/val/images")
    os.mkdir(new_dir + "/val/labels")


def rename_images(path, i=0):
    data = natsorted(os.listdir(path))
    print(len(data))
    for d in data:
        os.rename(path + d,
                  path + "image" + str(i) + ".jpg")
        i = i + 1


def rename_labels(path, i=0):
    data = natsorted(os.listdir(path))
    for d in data:
        os.rename(path + d,
                  path + "image" + str(i) + ".txt")
        i = i + 1


def create_list_from_categories(path_to_json):
    with open(path_to_json) as json_file:
        data = json.load(json_file)
    l = []
    val = list(data.values())
    for v in val:
        new_val = v.replace("suturo:", "").replace("soma:", "").replace("soma_home", "").replace("'", "")
        l.append(new_val)
    return l


# Write a function that combines 2 existing Datasets.
def combine_datasets(first, second, parent_dir, name, path_to_json_for_id):
    t1 = 0
    t2 = 0
    v1 = 0
    v2 = 0
    new_folder = os.path.join(parent_dir + name)
    create_new_dir(parent_dir, name)
    obj_list = create_list_from_categories(path_to_json_for_id)

    f = open(new_folder + "/data.yaml", "w+")
    f.write("train: " +  str(new_folder + "/train/images \n"))
    f.write("val: " + str(new_folder + "/val/images \n"))
    f.write("nc: " + str(len(obj_list)) + "\n")
    f.write("names: " + str(obj_list))
    if "train" in os.listdir(first):
        t1 = t1 + len(os.listdir(first + "/train/images"))
        print(t1)

    if "train" in os.listdir(second):
        t2 = t1 + len(os.listdir(second + "/train/images"))
        print(t2)

    if "val" in os.listdir(first):
        v1 = t2 + len(os.listdir(first + "/val/images"))
        print(v1)

    if "val" in os.listdir(second):
        v2 = v1 + len(os.listdir(second + "/val/images"))
        print(v2)

    for item in os.listdir(second + "/train/images"):
        shutil.copy(second + "/train/images/" + item, new_folder + "/train/images")

    for item in os.listdir(second + "/train/labels"):
        shutil.copy(second + "/train/labels/" + item, new_folder + "/train/labels")

    for item in os.listdir(second + "/val/images"):
        shutil.copy(second + "/val/images/" + item, new_folder + "/val/images")

    for item in os.listdir(second + "/val/labels"):
        shutil.copy(second + "/val/labels/" + item, new_folder + "/val/labels")

    rename_images(new_folder + "/train/images/", i=t1)
    rename_images(new_folder + "/val/images/", i=v1)
    rename_labels(new_folder + "/train/labels/", i=t1)
    rename_labels(new_folder + "/val/labels/", i=v1)

    for item in os.listdir(first + "/train/images"):
        shutil.copy(first + "/train/images/" + item, new_folder + "/train/images")

    for item in os.listdir(first + "/train/labels"):
        shutil.copy(first + "/train/labels/" + item, new_folder + "/train/labels")

    for item in os.listdir(first + "/val/images"):
        shutil.copy(first + "/val/images/" + item, new_folder + "/val/images")

    for item in os.listdir(first + "/val/labels"):
        shutil.copy(first + "/val/labels/" + item, new_folder + "/val/labels")

    rename_images(new_folder + "/train/images/")
    rename_images(new_folder + "/val/images/", i=t2)
    rename_labels(new_folder + "/train/labels/")
    rename_labels(new_folder + "/val/labels/", i=t2)