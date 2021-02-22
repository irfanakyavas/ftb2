import logging
from configparser import ConfigParser
from os import path
from typing import Dict

CONFIG_FILE_NAME = "ftb2.conf"
configuration_logger = logging.getLogger("[CONFIGURATION]")


class ConfigHandler:
    database_use = True
    disable_logging = False
    logging_level = 10
    database_address = "127.0.0.1"
    database_port = 3306
    database_name = "ftb2"
    database_username = "admin"
    database_password = "admin"

    def __init__(self):
        configuration_logger.info("Initializing configuration loader")
        config = ConfigParser()

        if path.exists(CONFIG_FILE_NAME):
            configuration_logger.info(f"Configuration file {CONFIG_FILE_NAME} already exists, trying to read.")
            config.read(CONFIG_FILE_NAME)
            ConfigHandler.database_use = config['DATABASE']['use_database']
            ConfigHandler.disable_logging = config['LOGGING']['disable_logging']
            ConfigHandler.logging_level = config['LOGGING']['logging_level']
            ConfigHandler.database_address = config['DATABASE']['database_address']
            ConfigHandler.database_port = config['DATABASE']['database_port']
            ConfigHandler.database_name = config['DATABASE']['database_name']
            ConfigHandler.database_username = config['DATABASE']['database_username']
            ConfigHandler.database_password = config['DATABASE']['database_password']
        else:
            configuration_logger.info(f"Configuration file {CONFIG_FILE_NAME} not found, writing default file.")
            print(f"No configuration file {CONFIG_FILE_NAME} found, writing default settings.")
            config['LOGGING'] = {'disable_logging': '0', 'logging_level': '10'}
            config['DATABASE'] = {'use_database': '1', 'database_address': '127.0.0.1', 'database_port': '3306',
                                  'database_name': 'ftb2', 'database_username': 'admin', 'database_password': 'admin'}
            with open(CONFIG_FILE_NAME, 'w') as configfile:
                config.write(configfile)

        configuration_logger.info("Program configuration completed.")
