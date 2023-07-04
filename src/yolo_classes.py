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

def change_class(directory=None):

    # Iterate over all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):  # Only process .txt files
            filepath = os.path.join(directory, filename)

            # Read the contents of the file
            with open(filepath, 'r') as file:
                contents = file.read()

            # Replace '52' with '1' in the file contents
            new_contents = contents.replace('50', '1')

            # Write the modified contents back to the file
            with open(filepath, 'w') as file:
                file.write(new_contents)

change_class("/home/sorin/data/tableware_objects2/val/labels")
#dir = "/home/sorin/data/seg-test/labels/"
#remove_class(dir, 10000)