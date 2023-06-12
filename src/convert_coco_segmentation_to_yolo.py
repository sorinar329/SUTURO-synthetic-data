import json

def data_finder():
    f = open("/home/sorin/code/blenderproc/output2/coco_data/coco_annotations.json")
    data = json.load(f)
    anns = data["annotations"]
    lines =[]
    i = 0
    for ann in anns:
        img_id = ann["image_id"]
        if img_id == i:
            segs = ann["segmentation"]["counts"]
            print(segs)
            id = ann["category_id"]
            new_segs = []
            for seg in segs:
                seg_relative = seg / 512
                new_segs.append(seg_relative)
            del new_segs[0]
            del new_segs[-1]
            new_segs_1 = str(new_segs).replace('[', '').replace(']', '').replace(',', '')
            line = str(id) + " " + str(new_segs_1) + "\n"
            lines.append(line)
        elif img_id == i + 1:
            print("a")
            with open(
                    '/home/sorin/data/blenderproc/data/yolo_dataset/13-04-2023/labels/image' + str(img_id - 1) + '.txt',
                    'w') as f:
                for line in lines:
                    f.write(line)
            segs = ann["segmentation"]["counts"]
            lines = []
            print(segs)
            id = ann["category_id"]
            new_segs = []
            for seg in segs:
                seg_relative = seg / 512
                new_segs.append(seg_relative)
            del new_segs[0]
            del new_segs[-1]
            new_segs_1 = str(new_segs).replace('[', '').replace(']', '').replace(',', '')
            line = str(id) + " " + str(new_segs_1) + "\n"
            lines.append(line)
            i = i + 1

data_finder()