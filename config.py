import configparser

def get_config(section, option):
    config = configparser.ConfigParser()
    config.read("config.ini", encoding="utf-8")
    return config.get(section, option)

def set_config(section, option, value):
    config = configparser.ConfigParser()
    config.read("config.ini")
    config[section][option] = value

    with open("config.ini", "w") as fp:
        config.write(fp)
    