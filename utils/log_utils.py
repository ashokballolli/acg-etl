import logging
import yaml


def setup_logging(config_file):
    configs = yaml.load(open(config_file), Loader=yaml.BaseLoader)
    log_config = configs['log']
    logging.basicConfig(filename=log_config['file_path'], level=log_config['level'],
                        format='%(asctime)s - %(levelname)s - %(message)s')
