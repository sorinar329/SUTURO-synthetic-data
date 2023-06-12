import os

def remove_class(dir, class_id):
    for file in os.listdir(dir):
        with open(dir + file, 'r') as f:
            lines = f.readlines()
        with open(dir + file, "w") as f:
            for line in lines:
                if not line.startswith(str(class_id)):
                    f.write(line)
                    #print(line)
                else:
                    print(line)
                    pass


dir = "/home/sorin/data/combined/09_06_dataset/val/labels/"
remove_class(dir, 10000)