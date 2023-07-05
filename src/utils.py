import json
import os
import shutil
#from natsort import natsorted
#from sklearn.model_selection import train_test_split

def create_list_from_id2json(path='/home/suturo/Developer/blenderproc/SUTURO-synthetic-data/data/id2name.json'):
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

def convert_bbox_coco2yolo(img_width, img_height, bbox):
    # YOLO bounding box format: [x_center, y_center, width, height]
    # (float values relative to width and height of image)

    x_tl = bbox[0]
    y_tl = bbox[1]
    w = bbox[2]
    h = bbox[3]


    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0

    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]


def get_id_of_object(obj, path='/home/suturo/Developer/blenderproc/SUTURO-synthetic-data/data/id2name.json'):
    with open(path) as json_file:
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

def convert_coco_to_yolo(path_to_json, new_dir, j=0):
    f = open(path_to_json)
    data = json.load(f)
    anns = data["annotations"]
    lines = []
    i = 0
    os.makedirs(new_dir + "/labels/")
    for ann in anns:
        img_id = ann["image_id"]
        if img_id == i:
            bbox = ann["bbox"]
            c = convert_bbox_coco2yolo(640, 480, bbox)
            coordinates = str(c).replace('[', '').replace(']', '').replace(',', '')
            id = ann["category_id"]

            line = str(id) + " " + str(coordinates) + "\n"
            lines.append(line)

        elif img_id == i + 1:

            with open(new_dir + '/labels/image' + str(img_id - 1 + j) + '.txt', 'w') as f:
                for line in lines:
                    f.write(line)

            lines = []
            bbox = ann["bbox"]
            c = convert_bbox_coco2yolo(640, 480, bbox)
            coordinates = str(c).replace('[', '').replace(']', '').replace(',', '')
            id = ann["category_id"]

            line = str(id) + " " + str(coordinates) + "\n"
            lines.append(line)
            i = i + 1
        else:

            i = i + 1


def move_images_to_new_dir(old_dir, new_dir):

    os.makedirs(new_dir + "/images")

    for item in sorted(os.listdir(old_dir)):
        shutil.copy(old_dir + item, new_dir + "/images/" + item)

    print(len(sorted(os.listdir(old_dir))) - 1)
    print(sorted(os.listdir(new_dir + "/images"))[423])
    os.remove(new_dir + "/images/" + sorted(os.listdir(new_dir + "/images"))[len(sorted(os.listdir(old_dir))) - 1])


def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            assert False


def trainsplit(path_source):
    os.makedirs(path_source + "train/images")
    os.makedirs(path_source + "val/images")
    os.makedirs(path_source + "test/images")
    os.makedirs(path_source + "train/labels")
    os.makedirs(path_source + "val/labels")
    os.makedirs(path_source + "test/labels")
    images = [os.path.join(path_source + "images/", x) for x in
              os.listdir(path_source + "images/") if x[-3:] == "jpg"]
    annotations = [os.path.join(path_source + "labels/", x) for x in
                   os.listdir(path_source + "labels/") if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size=0.05,
                                                                                    random_state=1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations,
                                                                                  test_size=0.05, random_state=1)

    move_files_to_folder(train_images, path_source + "train/images")
    move_files_to_folder(val_images, path_source + "val/images")
    move_files_to_folder(test_images, path_source + "test/images")
    move_files_to_folder(train_annotations, path_source + "train/labels")
    move_files_to_folder(val_annotations, path_source + "val/labels")
    move_files_to_folder(test_annotations, path_source + "test/labels")

def write_data_yaml(path_to_json_for_id, new_folder):
    obj_list = create_list_from_categories(path_to_json_for_id)

    f = open(new_folder + "/data.yaml", "w+")
    f.write("train: " + str(new_folder + "/train/images \n"))
    f.write("val: " + str(new_folder + "/val/images \n"))
    f.write("nc: " + str(len(obj_list)) + "\n")
    f.write("names: " + str(obj_list))


# Write a function that combines 2 existing Datasets.
def combine_datasets(first, second, parent_dir, name, path_to_json_for_id):
    t1 = 0
    t2 = 0
    v1 = 0
    v2 = 0
    index1 = 0
    index2 = 0
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
        index1 = index1 + len(os.listdir(first + "/train/images"))

    if "train" in os.listdir(second):
        t2 = t1 + len(os.listdir(second + "/train/images"))
        index2 = index2 + len(os.listdir(second + "/test/images"))

    if "val" in os.listdir(first):
        v1 = v1 + len(os.listdir(first + "/val/images"))
        index1 = index1 + len(os.listdir(first + "/val/images"))



    if "val" in os.listdir(second):
        v2 = v1 + len(os.listdir(second + "/val/images"))
        index2 = index2 + len(os.listdir(second + "/val/images"))

    if "test" in os.listdir(first):
        v2 = v1 + len(os.listdir(first + "/test/images"))
        index1 = index1 + len(os.listdir(first + "/test/images"))

    if "test" in os.listdir(second):
        v2 = v1 + len(os.listdir(second + "/test/images"))
        index2 = index2 + len(os.listdir(second + "/test/images"))



    for item in os.listdir(second + "/train/images"):
        shutil.copy(second + "/train/images/" + item, new_folder + "/train/images")

    for item in os.listdir(second + "/train/labels"):
        shutil.copy(second + "/train/labels/" + item, new_folder + "/train/labels")

    for item in os.listdir(second + "/val/images"):
        shutil.copy(second + "/val/images/" + item, new_folder + "/val/images")

    for item in os.listdir(second + "/val/labels"):
        shutil.copy(second + "/val/labels/" + item, new_folder + "/val/labels")

    rename_images(new_folder + "/train/images/", i=index1)
    rename_images(new_folder + "/val/images/", i=index1)
    rename_labels(new_folder + "/train/labels/", i=index1)
    rename_labels(new_folder + "/val/labels/", i=index1)

    for item in os.listdir(first + "/train/images"):
        shutil.copy(first + "/train/images/" + item, new_folder + "/train/images")

    for item in os.listdir(first + "/train/labels"):
        shutil.copy(first + "/train/labels/" + item, new_folder + "/train/labels")

    for item in os.listdir(first + "/val/images"):
        shutil.copy(first + "/val/images/" + item, new_folder + "/val/images")

    for item in os.listdir(first + "/val/labels"):
        shutil.copy(first + "/val/labels/" + item, new_folder + "/val/labels")

    rename_images(new_folder + "/train/images/")
    rename_images(new_folder + "/val/images/")
    rename_labels(new_folder + "/train/labels/")
    rename_labels(new_folder + "/val/labels/")
