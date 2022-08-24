#!/usr/bin/env python3

import logging
import os
import subprocess
import sys

from utils.config import get_config, config_report
from utils.args import get_args
from utils.logg import config_logg
from utils.misc import cleanup


def main():
    cleanup()

    args = get_args()
    conf = get_config()

    # Config logging
    config_logg(conf["Logging"])

    # Prints the configuration used in this run
    config_report(conf)
    
    # Launch chain of subproceses:  slicer -> presorter -> consolidator
    p1 = subprocess.run([sys.executable,"main_slicer.py", 
               "-n", str(args.nbig), "-if", args.input_file, "-of", "dummy"])

    p2 = subprocess.run([sys.executable,"main_presorter.py", 
               "-n", str(args.nbig), "-if", args.input_file, "-of", "dummy"])

    p3 = subprocess.run([sys.executable,"main_consolidator.py", 
               "-n", str(args.nbig), "-if", args.input_file, 
               "-of", args.output_file])


if __name__ == "__main__":
    main()
