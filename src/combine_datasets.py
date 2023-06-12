import utils

# FIRST HAS TO BE THE BIGGER DATASET
def combine():
    first = "/home/sorin/data/combined/first3"
    second = "/home/sorin/data/09_06_storing_groceries"
    parent_dir = "/home/sorin/data/combined/"
    path_to_json_for_id = "/home/sorin/code/blenderproc/data/id2name.json"
    name = "09_06_dataset"
    utils.combine_datasets(first=first, name=name, second=second,
                           parent_dir=parent_dir, path_to_json_for_id=path_to_json_for_id)

combine()