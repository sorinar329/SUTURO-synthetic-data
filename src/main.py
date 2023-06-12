import argparse
import yaml_config
import os


def get_parse_args():
    parser = argparse.ArgumentParser(description='A test program.')
    parser.add_argument("--scene", help="Name of the python file to execute")
    parser.add_argument("--config_yaml", help="Config file which should be located at /data/yaml")
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_parse_args()
    config = yaml_config.YAMLConfig(args.config_yaml)
    os.system(f"blenderproc run {get_parse_args().scene}.py")
