import yaml
import filepaths


class YAMLConfig(object):
    def __init__(self, filename):
        config = filepaths.get_path_yaml_config(filename)
        with open(config, 'r') as stream:
            data_loaded = yaml.safe_load(stream)
        self._data = data_loaded

    def print(self):
        print(self._data)

    def get_list_positions(self):
        pos_dict = self._data['positions']
        return [v for k, v in pos_dict.items()]

    def get_list_locations(self):
        locations_dict = self._data['locations']
        return [v for k, v in locations_dict.items()]

    def get_position_of_interest(self):
        return self._data['position_of_interest']

    def get_objects(self):
        return self._data['objects']


