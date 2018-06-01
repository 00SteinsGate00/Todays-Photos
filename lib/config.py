import datetime
import json


class Config:

    def __init__(self, config_file):
        # open the file and parse the json
        cfg_fp = open(config_file, 'r')
        cfg_json = json.load(cfg_fp)
        cfg_fp.close()

        # read the properties
        self.source_dir      = cfg_json['source_dir']
        self.destination_dir = cfg_json['destination_dir']
        self.export_folder   = cfg_json['export_folder']
        self.target_folders  = cfg_json['target_folders']
        self.date_format     = cfg_json['date_format']
        self.delimiter       = cfg_json['export_folder_delimiter'] if 'export_folder_delimiter' in cfg_json.keys() else ' '
