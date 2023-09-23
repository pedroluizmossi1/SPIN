import configparser

CONFIG_FILE = 'config.ini'

config = configparser.ConfigParser()

config.read(CONFIG_FILE)

def get_config(section, key):
    return config[section][key]

def update_config(section, key, value):
    config.set(section, key, value)
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)