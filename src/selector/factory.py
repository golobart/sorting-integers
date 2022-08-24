import logging
import sys

from selector.py_array_insort import PyArrayInSsort
from selector.py_array_insort2 import PyArrayInSsort2
from selector.py_array_preall import PyArrayPreall
from selector.py_list import PyListSelector


def selector_factory(conf):
    """
    Selects the selector object to create according the config.

    Args:
        conf: Dict of the General section of the config file.
    Returns:
        selector: Reference to the object selector.
    """
    st = conf["store_top"]
    logging.debug(f"selector_factory store_top  = {st}")
    if st == "py_array_insort":
        logging.debug(f"selector_factory PyArrayInSsort selected")
        selector = PyArrayInSsort
    elif st == "py_array_insort2":
        logging.debug(f"selector_factory PyArrayInSsort2 selected")
        selector = PyArrayInSsort2
    elif st == "py_array_preall":
        logging.debug(f"selector_factory PyArrayPreall selected")
        selector = PyArrayPreall
    elif st == "py_list":
        logging.debug(f"selector_factory PyListSelector selected")
        selector = PyListSelector
    elif st == "np_array":
        logging.debug(f"selector_factory NPArraySelector selected")
        selector = NPArraySelector
    else:
        raise ValueError(f"Unknow store type {st}")
    return selector


def get_selector(args, conf):
    """
    Returns the selector object created by the factory.

    Args:
        args: Command line arguments
        conf: Dict of the General section of the config file.
    Returns:
        The object selector.
    """
    factory_obj = None
    try:
        factory_obj = selector_factory(conf)
    except ValueError as e:
        logging.critical(e)
        sys.exit()
    except Exception as err:
        logging.error(f"Unexpected {err=}, {type(err)=}")
        raise

    return factory_obj(args, conf)