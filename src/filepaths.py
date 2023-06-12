from pathlib import Path


def get_path_id2name_json():
    p = Path.cwd().joinpath("../", "data", "id2name.json")
    if not p.exists():
        raise Exception("id2name.json doesn't exist")
    return Path.cwd().joinpath("../", "data", "id2name.json")


def get_path_yaml_config(filename):
    p = Path.cwd().joinpath("../", "data/yaml", filename)
    if p.suffix != ".yaml":
        p = p.with_suffix(".yaml")
        if p.is_file():
            return p
        else:
            raise Exception("File doesn't exist")

    if not p.is_file():
        raise Exception("File doesn't exist")
    return p


def get_path_blender_scene(path_to_project: str, blend_scene: str):
    p = Path(path_to_project).joinpath("scenes", blend_scene)
    if p.suffix != ".blend":
        raise Exception(f"Expected .blend file, got {p.suffix}")
    return p


def get_project_src_dir():
    return Path.cwd()


def get_path_output_dir():
    p = Path.cwd().joinpath("../", "output")
    if not p.exists():
        Path(p).mkdir(parents=True)
    return p
