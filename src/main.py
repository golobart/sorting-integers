#!/usr/bin/env python3

import logging

from utils.config import get_config, config_report
from utils.args import get_args
from utils.logg import config_logg
from selector.factory import get_selector

def main():
    args = get_args()
    conf = get_config()

    # Config logging
    config_logg(conf["Logging"])

    # Prints the configuration used in this run
    config_report(conf)
    
    selector = get_selector(args, conf["General"])

    # create sorted array
    selector.select_nbig()

    # write the sorted file:
    logging.debug(f"Array topn to file")
    selector._write_output_file(selector.outfilename)

    selector.result_report()
    #logging.info(selector.topn)


if __name__ == "__main__":
    main()
