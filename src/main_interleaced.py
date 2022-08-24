#!/usr/bin/env python3

import logging
import os
import subprocess
import sys, time

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
    
    # Launch chain of subproceses: 1 slicer + 1 presorter + 1 consolidator
    p1 = subprocess.Popen([sys.executable,"main_slicer.py", 
               "-n", str(args.nbig), "-if", args.input_file, "-of", "dummy"])

    p21 = subprocess.Popen([sys.executable,"main_presorter.py", 
               "-n", str(args.nbig), "-if", args.input_file, "-of", "dummy"])

    p3 = subprocess.Popen([sys.executable,"main_consolidator.py", 
               "-n", str(args.nbig), "-if", args.input_file, 
               "-of", args.output_file])

    # wait for subproceses to terminate
    p1.wait()
    p21.wait()
    p3.wait()


if __name__ == "__main__":
    main()
