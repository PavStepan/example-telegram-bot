from configparser import ConfigParser


def get_db_config(filename='config.ini', section='postgresql') -> dict:
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


def get_bot_token(filename='config.ini', section='telegram') -> str:
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        api_token = params[0][1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return api_token


def get_web_url(filename='config.ini', section='web') -> str:
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    if parser.has_section(section):
        params = parser.items(section)
        url_web = params[0][1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return url_web
