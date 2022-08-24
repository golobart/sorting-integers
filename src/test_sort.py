import unittest
import array as arr

from selector import py_array_insort, py_array_insort2, py_array_preall, py_list
#import src.selector as sel

def in_generator(iter):
    for i in iter:
        yield(i)

class p_args(object):
    nbig = 10
    input_file = "in1"
    output_file = "out1"


class TestSort(unittest.TestCase):
    in_list = ["43", "75", "10234234", "pepe", "2", "1", "  300000  ", "200000", "31500", "70", "11", "150", "-34", "345 11"]
    out_arr = arr.array("Q", [2, 11, 43, 70, 75, 150, 31500, 200000, 300000, 10234234])
    

    def test_insort(self):
        """
        Test sorting a short list by PyArrayInSsort
        """
        par_list = [43, 75, 10234234, 2, 1, 300000, 200000, 31500, 70, 11, 150]
        par_out = arr.array("Q", [10234234, 300000, 200000, 31500, 150, 75, 70, 43, 11, 2])
        #out_arr = arr.array("Q", [2, 11, 43, 70, 75, 150, 31500, 200000, 300000, 10234234])
        conf_dict = {"allow_repeats": "0", "filebuffer": "65536"}
        elements = in_generator(par_list)
        
        selector = py_array_insort.PyArrayInSsort(p_args, conf_dict)
        selector.select_nbig(elements)

        self.assertEqual(selector.topn, par_out)


    def test_insort2(self):
        """
        Test sorting a short list by PyArrayInSsort2
        """
        #in_list = ["43", "75", "10234234", "pepe", "2", "1", "300000", "200000", "31500", "70", "11", "150"]
        #out_arr = arr.array("Q", [2, 11, 43, 70, 75, 150, 31500, 200000, 300000, 10234234])
        conf_dict = {"allow_repeats": "0", "filebuffer": "65536"}
        elements = in_generator(self.in_list)

        selector = py_array_insort2.PyArrayInSsort2(p_args, conf_dict)
        selector.select_nbig(elements)

        self.assertEqual(selector.topn, self.out_arr)


    def test_preall(self):
        """
        Test sorting a short list by PyArrayPreall
        """
        #in_list = ["43", "75", "10234234", "pepe", "2", "1", "300000", "200000", "31500", "70", "11", "150"]
        #out_arr = arr.array("Q", [2, 11, 43, 70, 75, 150, 31500, 200000, 300000, 10234234])
        conf_dict = {"allow_repeats": "0", "filebuffer": "65536"}
        elements = in_generator(self.in_list)
        
        selector = py_array_preall.PyArrayPreall(p_args, conf_dict)
        selector.select_nbig(elements)

        self.assertEqual(selector.topn, self.out_arr)


if __name__ == '__main__':
    unittest.main()