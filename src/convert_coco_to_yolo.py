import os

import cv2
import json
import shutil
from sklearn.model_selection import train_test_split


def test():
    x0 = 70
    x1 = 70 + 38
    y0 = 199 + 74
    y1 = 199
    img = cv2.imread('/home/sorin/data/blenderproc/output/coco_data/images/000023.jpg')
    start_point = (int(x0), int(y0))
    end_point = (int(x1), int(y1))
    cv2.rectangle(img, start_point, end_point, color=(0, 255, 0))
    cv2.imshow("abc", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def convert_bbox_coco2yolo(img_width, img_height, bbox):
    # YOLO bounding box format: [x_center, y_center, width, height]
    # (float values relative to width and height of image)
    # print(bbox)
    x_tl = bbox[0]
    y_tl = bbox[1]
    w = bbox[2]
    h = bbox[3]

    # print(x_tl, y_tl, w, h)
    dw = 1.0 / img_width
    dh = 1.0 / img_height

    x_center = x_tl + w / 2.0
    y_center = y_tl + h / 2.0

    x = x_center * dw
    y = y_center * dh
    w = w * dw
    h = h * dh

    return [x, y, w, h]


def convert_coco_to_yolo():
    f = open("/first_dataset_18_objects_on_table_7k/coco_data/coco_annotations.json")
    data = json.load(f)
    anns = data["annotations"]
    i = 0
    lines = []
    for ann in anns:
        img_id = ann["image_id"]
        if img_id == i:
            bbox = ann["bbox"]
            c = convert_bbox_coco2yolo(512, 512, bbox)
            coordinates = str(c).replace('[', '').replace(']', '').replace(',', '')
            id = ann["category_id"]
            print(str(id) + " " + coordinates)
            line = str(id) + " " + str(coordinates) + "\n"
            lines.append(line)
            print("c")
        elif img_id == i + 1:
            print("a")
            with open('/home/sorin/data/blenderproc/data/yolo_dataset/12-04-2023/labels/image' + str(img_id - 1) + '.txt', 'w') as f:
                for line in lines:
                    f.write(line)
            print(lines)
            lines = []
            bbox = ann["bbox"]
            c = convert_bbox_coco2yolo(512, 512, bbox)
            coordinates = str(c).replace('[', '').replace(']', '').replace(',', '')
            id = ann["category_id"]
            print(str(id) + " " + coordinates)
            line = str(id) + " " + str(coordinates) + "\n"
            lines.append(line)
            i = i + 1


def rename_images():
    data = sorted(os.listdir("/home/sorin/data/blenderproc/data/yolo_dataset/13-04-2023/images"))
    i = 0
    for d in data:
        os.rename("/home/sorin/data/blenderproc/data/yolo_dataset/13-04-2023/images/" + d,
                  "/home/sorin/data/blenderproc/data/yolo_dataset/13-04-2023/images/" + "image" + str(i) + ".jpg")
        i = i + 1


def create_list_from_categories():
    with open("/home/sorin/code/blenderproc/data/id2name.json") as json_file:
        data = json.load(json_file)
    l = []
    val = list(data.values())
    for v in val:
        new_val = v.replace("suturo:", "").replace("soma:", "").replace("soma_home", "").replace("'", "")
        l.append(new_val)
    print(l)
    print(len(l))


#convert_coco_to_yolo()
#rename_images()
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False


def trainsplit(path_source):
    images = [os.path.join(path_source + "images/", x) for x in
              os.listdir(path_source + "images/") if x[-3:] == "jpg"]
    print(images)
    annotations = [os.path.join(path_source + "labels/", x) for x in
                   os.listdir(path_source + "labels/") if x[-3:] == "txt"]

    images.sort()
    annotations.sort()

    # Split the dataset into train-valid-test splits
    train_images, val_images, train_annotations, val_annotations = train_test_split(images, annotations, test_size=0.2,
                                                                                    random_state=1)
    val_images, test_images, val_annotations, test_annotations = train_test_split(val_images, val_annotations,
                                                                                  test_size=0.5, random_state=1)

    move_files_to_folder(train_images, path_source + "train/images")
    move_files_to_folder(val_images, path_source + "val/images")
    move_files_to_folder(test_images, path_source + "test/images")
    move_files_to_folder(train_annotations, path_source + "train/labels")
    move_files_to_folder(val_annotations, path_source + "val/labels")
    move_files_to_folder(test_annotations, path_source + "test/labels")


#trainsplit(path_source="/home/sorin/data/blenderproc/data/yolo_dataset/13-04-2023/")
#create_list_from_categories()
#convert_coco_to_yolo()
#rename_images()
def pipeline():
    # mkdir for the dataset with the name based by date
    #convert_coco_to_yolo() #convert from output coco
    # cp images from output to new created directory
    rename_images() #rename images to make them consistent to the annotations
    trainsplit(path_source="/home/sorin/data/blenderproc/data/yolo_dataset/13-04-2023/")
    # trainsplit() needs more parametrization
    # create data.yaml for the training
    # optional start training

pipeline()