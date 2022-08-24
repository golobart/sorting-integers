import logging


def config_logg(cnf):
    """
    Configures basic logging.

    Logging output can be configured to file or to console, depends on conf param enable
    
    Args:
        cnf (dict): Dictionary with entries suitable to basicConfig log function.
    """
    # Get the numeric level
    nlevel = getattr(logging, cnf["level"].upper())

    # make a copy of the config log dict
    cf = dict(cnf)
    # Remove invalid entry
    cf.pop("enable")
    cf["level"] = nlevel

    if not bool(int(cnf["enable"])):
        # Remove entries only valid for log file, output to console not to file
        cf.pop("filename")
        cf.pop("filemode")

    logging.basicConfig(**cf)
