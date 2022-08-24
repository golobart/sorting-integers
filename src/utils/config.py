import logging
import configparser


def get_config(config_path: str ='config/config.ini'):
    """
    Loads configuration data from ini file.

    Args:
        config_path (str): Path to configuration file.
    Returns:
        config (ConfigParser): ConfigParser instance containing the loaded configuration values.
    Note:
        config values can be read as config["General"]["fileBuffer"]
    """
    config = configparser.ConfigParser()
    config.read(config_path)

    return config


def config_report(config):
    """
    Prints configuration to log.

    Only General section is printed.
    Args:
        config: The config parser to print.
    """
    logging.info("-------------Config report-------------------------")
    logging.info(f"Chunk of file in memory filebuffer = {config['General']['filebuffer']}")
    logging.info(f"Repetitions allowed? {bool(int(config['General']['allow_repeats']))}")
    logging.info(f"Type of store {config['General']['store_top']}")
    logging.info("---------------------------------------------------")