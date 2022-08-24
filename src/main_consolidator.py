#!/usr/bin/env python3

import logging

from utils.config import get_config, config_report
from utils.args import get_args
from utils.logg import config_logg
from consolidator.consolidator import Consolidator

def main():
    args = get_args()
    conf = get_config()

    # Config logging
    config_logg(conf["Logging"])

    # # Prints the configuration used in this run
    # config_report(conf)

    c = Consolidator(args, conf["General"])
    c.consolidate_pool()

if __name__ == "__main__":
    main()
