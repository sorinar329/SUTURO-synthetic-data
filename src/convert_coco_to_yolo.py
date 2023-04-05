import os

import cv2
import json
# [70, 199, 38, 74]

def test():
    x0 = 70
    x1 = 70 + 38
    y0 = 199 + 74
    y1 = 199
    img = cv2.imread('/home/sorin/data/blenderproc/output/coco_data/images/000023.jpg')
    start_point = (int(x0), int(y0))
    end_point = (int(x1), int(y1))
    cv2.rectangle(img, start_point, end_point, color=(0,255,0))
    cv2.imshow("abc", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#test()
def convert_bbox_coco2yolo(img_width, img_height, bbox):
    # YOLO bounding box format: [x_center, y_center, width, height]
    # (float values relative to width and height of image)
    print(bbox)
    x_tl = bbox[0]
    y_tl = bbox[1]
    w = bbox[2]
    h = bbox[3]

    print(x_tl, y_tl, w, h)
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
    f = open("/home/sorin/data/blenderproc/output/coco_data/coco_annotations.json")
    data = json.load(f)
    anns = data["annotations"]

    j = 0
    i = 0
    lines = []
    for ann in anns:
        img = ann["image_id"]
        label = ann["category_id"]
        if img < 181:
            if img == i:
                if label == 2 or label == 5 or label == 10 or label == 12 or label == 6 or label == 4:
                    bbox = ann["bbox"]
                    c = convert_bbox_coco2yolo(512, 512, bbox)
                    coordinates = str(c).replace('[', '').replace(']', '').replace(',', '')
                    id = ann["category_id"] - 1
                    print(str(id) + " " + coordinates)
                    line = str(id) + " " + str(coordinates) + "\n"
                    lines.append(line)

                with open('/home/sorin/code/blenderproc/data/yolo_dataset/03-04-2023/image' + str(img) + '.txt', 'w') as f:
                    for line in lines:
                        f.write(line)
            else:
                i = i + 1
                lines = []


def rename_images():
    data = sorted(os.listdir("/home/sorin/data/blenderproc/data/yolo_dataset/03-04-2023/images"))
    i = 0

    for d in data:
        os.rename("/home/sorin/data/blenderproc/data/yolo_dataset/03-04-2023/images/" + d,
                    "/home/sorin/data/blenderproc/data/yolo_dataset/03-04-2023/images/" + "image" + str(i) + ".jpg")

        i = i + 1


def create_list_from_categories():
    obj_list = []
    f = open("/home/sorin/data/blenderproc/output/coco_data/coco_annotations.json")
    data = json.load(f)
    catas = data["categories"]
    for cat in catas:
        obj_list.append(cat["name"])

    print(obj_list)
    print(len(obj_list))

convert_coco_to_yolo()