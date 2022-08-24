import logging
import bisect


class PyListSelector():
    """
    Selector of topnumbers based on python list.

    Lists support elements of different types and contiguous in memory is not guaranted.
    """

    def __init__(self, args, conf):
        topn = []
        for x in [3, 1, 1, 70, 300, 4, 45, 200, 45, 46, 2, 150, 0, 100, 300, 1700]:
            index = bisect.bisect_right(topn, x)
            logging.debug(f"{index=}")
            num_elems = len(topn)
            logging.debug(f"{num_elems=}")
            if not num_elems:
                topn.append(x)
                logging.debug(f"FIRST {x=} {topn=}")
                continue
            if topn[index-1] == x: # is a repetition
                if bool(int(conf["allow_repeats"])):
                    if  args.nbig > len(topn):
                        if index < num_elems:
                            topn.insert(index, x)
                        else:
                            topn.append(x)
                        logging.debug(f"REPETITION topn growing {x=} {topn=}")
                    else:
                        if index < num_elems:
                            topn.insert(index, x)
                        else:
                            topn.append(x)
                        topn.pop(0)
                        logging.debug(f"REPETITION topn full {x=} {topn=}")
                else:
                    logging.debug(f"REPETITION NOT allowed {x=} {topn=}")
            else:
                if  args.nbig > len(topn):
                    if index < num_elems:
                        topn.insert(index, x)
                    else:
                        topn.append(x)
                    logging.debug(f"NO REP topn growing {x=} {topn=}")
                else:
                    if index < num_elems:
                        topn.insert(index, x)
                    else:
                        topn.append(x)
                    topn.pop(0)
                    logging.debug(f"NO REP topn full {x=} {topn=}")

            #    write to topn (control repetitions)
            # else:
            #    if value>= min_value_in_topn:
            #        write to topn (control repetitions)
            #index = bisect_left(topn, x, lo=0, hi=len(a), *, key=None)
            
            # logging.debug(f"{x=}")
            # logging.debug(f"{index=}")
            # topn.insert(index, x)
            # logging.debug(f"{topn=}")
            # logging.debug(f"{topn.buffer_info()=}")

    

    def get_topn(self):
        pass